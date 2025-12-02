"""
Property-based tests for AccessRequest model
Feature: user1-supervisor-management
"""
import pytest
from hypothesis import given, strategies as st, settings, assume
from datetime import date, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from core.models import AccessRequest, User, Company


@pytest.mark.django_db(transaction=True)
class TestAccessRequestProperties:
    """Property-based tests for AccessRequest"""
    
    @settings(max_examples=100, deadline=None)
    @given(
        has_ep_no=st.booleans(),
        has_access_type=st.booleans(),
        has_justification=st.booleans(),
        access_type=st.sampled_from(['date_range', 'permanent']),
        has_dates=st.booleans(),
        dates_valid=st.booleans()
    )
    def test_property_5_request_validation_rules(
        self, has_ep_no, has_access_type, has_justification, 
        access_type, has_dates, dates_valid
    ):
        """
        Feature: user1-supervisor-management, Property 5: Request Validation Rules
        Validates: Requirements 3.2, 3.3, 3.4
        
        For any access request, it should be valid if and only if:
        (1) it includes EP NO, access type, and justification,
        (2) date range requests include start and end dates, and
        (3) permanent requests do not require dates.
        """
        # Create test data
        company, _ = Company.objects.get_or_create(name="Test Company")
        
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        user, _ = User.objects.get_or_create(
            username=f"testuser_{unique_id}",
            defaults={'role': 'user1', 'company': company}
        )
        
        # Build request data based on test parameters
        today = timezone.now().date()
        
        request_data = {
            'requester': user,
            'company': company,
        }
        
        if has_ep_no:
            request_data['ep_no'] = "EMP001"
        else:
            request_data['ep_no'] = ""  # Empty EP NO
        
        if has_access_type:
            request_data['access_type'] = access_type
        else:
            request_data['access_type'] = 'date_range'  # Default
        
        if has_justification:
            request_data['justification'] = "Test justification"
        else:
            request_data['justification'] = ""  # Empty justification
        
        # Handle dates based on access type
        if request_data['access_type'] == 'date_range':
            if has_dates:
                if dates_valid:
                    request_data['access_from'] = today
                    request_data['access_to'] = today + timedelta(days=30)
                else:
                    # Invalid: end before start
                    request_data['access_from'] = today + timedelta(days=30)
                    request_data['access_to'] = today
            # else: dates are None (missing)
        else:  # permanent
            # Permanent requests don't need dates
            request_data['access_from'] = None
            request_data['access_to'] = None
        
        # Create request and validate
        request = AccessRequest(**request_data)
        
        # Determine if request should be valid
        should_be_valid = True
        
        # Rule 1: Must have EP NO, access type, and justification
        if not has_ep_no or not has_justification:
            should_be_valid = False
        
        # Rule 2: Date range requests must have both dates
        if request_data['access_type'] == 'date_range':
            if not has_dates:
                should_be_valid = False
            elif has_dates and not dates_valid:
                should_be_valid = False
        
        # Test validation
        if should_be_valid:
            try:
                request.full_clean()
                # Should not raise exception
                assert True
            except ValidationError as e:
                pytest.fail(f"Request should be valid but raised ValidationError: {e}")
        else:
            # Should raise ValidationError
            with pytest.raises(ValidationError):
                request.full_clean()

    
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
        from core.services.request_approval_service import RequestApprovalService
        
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
        
        # Create dates based on access type
        if access_type == 'date_range':
            dates = {
                'access_from': today,
                'access_to': today + timedelta(days=days_duration)
            }
        else:
            dates = {}
        
        # Create request
        requests = RequestApprovalService.create_request(
            user=user,
            ep_nos=[ep_no],
            access_type=access_type,
            dates=dates,
            justification="Test request"
        )
        
        request = requests[0]
        
        # Approve request
        assignment = RequestApprovalService.approve_request(request.id, admin)
        
        # Property: Assignment should exist with matching details
        assert assignment is not None, "Assignment should be created"
        assert assignment.user == user, "Assignment user should match requester"
        assert assignment.ep_no == ep_no, "Assignment EP NO should match request"
        assert assignment.company == company, "Assignment company should match"
        assert assignment.source == 'request', "Assignment source should be 'request'"
        assert assignment.is_active == True, "Assignment should be active"
        
        if access_type == 'date_range':
            assert assignment.access_from == dates['access_from'], "Access from should match"
            assert assignment.access_to == dates['access_to'], "Access to should match"
        else:
            assert assignment.access_from is None, "Permanent access should have no start date"
            assert assignment.access_to is None, "Permanent access should have no end date"

    
    @settings(max_examples=50, deadline=None)
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
        from core.services.request_approval_service import RequestApprovalService
        
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
        requests = RequestApprovalService.create_request(
            user=user,
            ep_nos=[f"EMP_{unique_id}"],
            access_type='permanent',
            dates={},
            justification="Test request"
        )
        
        request = requests[0]
        
        # Reject request
        reason = "Test rejection reason" if has_reason else ""
        rejected_request = RequestApprovalService.reject_request(request.id, admin, reason)
        
        # Property: Status should be rejected
        assert rejected_request.status == 'rejected', "Status should be 'rejected'"
        assert rejected_request.reviewed_by == admin, "Reviewed by should be admin"
        assert rejected_request.reviewed_at is not None, "Reviewed at should be set"
        
        if has_reason:
            assert rejected_request.rejection_reason == reason, "Rejection reason should match"
        else:
            assert rejected_request.rejection_reason == "", "Rejection reason should be empty"
