"""
Property-based tests for RequestApprovalService
Feature: user1-supervisor-management
"""
import pytest
from hypothesis import given, strategies as st, settings
from datetime import timedelta
from django.utils import timezone
from core.models import AccessRequest, EmployeeAssignment, User, Company, AccessRequestAuditLog
from core.services.request_approval_service import RequestApprovalService


@pytest.mark.django_db(transaction=True)
class TestRequestApprovalProperties:
    """Property-based tests for RequestApprovalService"""
    
    @settings(max_examples=100, deadline=None)
    @given(
        access_type=st.sampled_from(['date_range', 'permanent']),
        days_duration=st.integers(min_value=1, max_value=90)
    )
    def test_property_9_approval_creates_assignment(self, access_type, days_duration):
        """
        Feature: user1-supervisor-management, Property 9: Approval Creates Assignment
        Validates: Requirements 4.3
        
        For any approved access request, an employee assignment should exist
        with matching User1, EP NO, and date range details.
        """
        # Create test data
        company, _ = Company.objects.get_or_create(name="Test Company")
        
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        user, _ = User.objects.get_or_create(
            username=f"user1_{unique_id}",
            defaults={'role': 'user1', 'company': company}
        )
        admin, _ = User.objects.get_or_create(
            username=f"admin_{unique_id}",
            defaults={'role': 'admin', 'company': company}
        )
        
        today = timezone.now().date()
        ep_no = f"EMP_{unique_id}"
        
        # Create request
        if access_type == 'date_range':
            access_from = today
            access_to = today + timedelta(days=days_duration)
        else:
            access_from = None
            access_to = None
        
        request = AccessRequest.objects.create(
            requester=user,
            ep_no=ep_no,
            company=company,
            access_type=access_type,
            access_from=access_from,
            access_to=access_to,
            justification="Test request",
            status='pending'
        )
        
        # Approve request
        assignment = RequestApprovalService.approve_request(request.id, admin)
        
        # Property: Assignment should exist with matching details
        assert assignment is not None
        assert assignment.user == user
        assert assignment.ep_no == ep_no
        assert assignment.access_from == access_from
        assert assignment.access_to == access_to
        assert assignment.source == 'request'
        assert assignment.is_active == True
        
        # Verify request status updated
        request.refresh_from_db()
        assert request.status == 'approved'
        assert request.reviewed_by == admin
    
    @settings(max_examples=100, deadline=None)
    @given(
        has_reason=st.booleans()
    )
    def test_property_10_rejection_updates_status(self, has_reason):
        """
        Feature: user1-supervisor-management, Property 10: Rejection Updates Status
        Validates: Requirements 4.4
        
        For any rejected access request, its status should be "rejected"
        and optionally include a rejection reason.
        """
        # Create test data
        company, _ = Company.objects.get_or_create(name="Test Company")
        
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        user, _ = User.objects.get_or_create(
            username=f"user1_{unique_id}",
            defaults={'role': 'user1', 'company': company}
        )
        admin, _ = User.objects.get_or_create(
            username=f"admin_{unique_id}",
            defaults={'role': 'admin', 'company': company}
        )
        
        # Create request
        request = AccessRequest.objects.create(
            requester=user,
            ep_no=f"EMP_{unique_id}",
            company=company,
            access_type='permanent',
            justification="Test request",
            status='pending'
        )
        
        # Reject request
        reason = "Test rejection reason" if has_reason else ""
        rejected_request = RequestApprovalService.reject_request(request.id, admin, reason)
        
        # Property: Status should be rejected
        assert rejected_request.status == 'rejected'
        assert rejected_request.reviewed_by == admin
        assert rejected_request.reviewed_at is not None
        
        if has_reason:
            assert rejected_request.rejection_reason == reason
        else:
            assert rejected_request.rejection_reason == ""
    
    @settings(max_examples=50, deadline=None)
    @given(
        num_requests=st.integers(min_value=1, max_value=5)
    )
    def test_property_24_audit_log_completeness(self, num_requests):
        """
        Feature: user1-supervisor-management, Property 24: Audit Log Completeness
        Validates: Requirements 9.1, 9.2, 9.5
        
        For any access request or assignment change, a corresponding audit log entry
        should exist with timestamp and actor information.
        """
        # Create test data
        company, _ = Company.objects.get_or_create(name="Test Company")
        
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        user, _ = User.objects.get_or_create(
            username=f"user1_{unique_id}",
            defaults={'role': 'user1', 'company': company}
        )
        admin, _ = User.objects.get_or_create(
            username=f"admin_{unique_id}",
            defaults={'role': 'admin', 'company': company}
        )
        
        # Create multiple requests
        ep_nos = [f"EMP_{unique_id}_{i}" for i in range(num_requests)]
        
        requests = RequestApprovalService.create_request(
            user=user,
            ep_nos=ep_nos,
            access_type='permanent',
            dates={},
            justification="Test bulk request"
        )
        
        # Property: Each request should have a creation log entry
        for request in requests:
            log_entries = AccessRequestAuditLog.objects.filter(
                action='request_created',
                target_ep_no=request.ep_no,
                actor=user
            )
            assert log_entries.exists(), f"No audit log for request {request.id}"
            
            log_entry = log_entries.first()
            assert log_entry.timestamp is not None
            assert log_entry.actor == user
        
        # Approve first request
        if requests:
            RequestApprovalService.approve_request(requests[0].id, admin)
            
            # Should have approval and assignment creation logs
            approval_logs = AccessRequestAuditLog.objects.filter(
                action='request_approved',
                target_ep_no=requests[0].ep_no
            )
            assert approval_logs.exists()
            
            assignment_logs = AccessRequestAuditLog.objects.filter(
                action='assignment_created',
                target_ep_no=requests[0].ep_no
            )
            assert assignment_logs.exists()
