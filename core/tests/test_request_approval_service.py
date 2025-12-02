"""
Unit tests for RequestApprovalService
"""
import pytest
from django.utils import timezone
from core.models import AccessRequest, User, Company
from core.services.request_approval_service import RequestApprovalService


@pytest.mark.django_db
class TestRequestApprovalService:
    """Unit tests for RequestApprovalService"""
    
    def test_cannot_approve_already_processed_request(self):
        """Test cannot approve already-processed request"""
        company = Company.objects.create(name="Test Company")
        user = User.objects.create_user(
            username="user1_test",
            role="user1",
            company=company
        )
        admin = User.objects.create_user(
            username="admin_test",
            role="admin",
            company=company
        )
        
        # Create and approve request
        request = AccessRequest.objects.create(
            requester=user,
            ep_no="EMP001",
            company=company,
            access_type='permanent',
            justification="Test",
            status='pending'
        )
        
        RequestApprovalService.approve_request(request.id, admin)
        
        # Try to approve again
        with pytest.raises(ValueError, match="cannot be approved"):
            RequestApprovalService.approve_request(request.id, admin)
    
    def test_cancelling_pending_request(self):
        """Test cancelling pending request"""
        company = Company.objects.create(name="Test Company")
        user = User.objects.create_user(
            username="user1_test",
            role="user1",
            company=company
        )
        
        # Create request
        request = AccessRequest.objects.create(
            requester=user,
            ep_no="EMP001",
            company=company,
            access_type='permanent',
            justification="Test",
            status='pending'
        )
        
        # Cancel request
        cancelled = RequestApprovalService.cancel_request(request.id, user)
        
        assert cancelled.status == 'cancelled'
    
    def test_cannot_cancel_approved_request(self):
        """Test cannot cancel approved request"""
        company = Company.objects.create(name="Test Company")
        user = User.objects.create_user(
            username="user1_test",
            role="user1",
            company=company
        )
        admin = User.objects.create_user(
            username="admin_test",
            role="admin",
            company=company
        )
        
        # Create and approve request
        request = AccessRequest.objects.create(
            requester=user,
            ep_no="EMP001",
            company=company,
            access_type='permanent',
            justification="Test",
            status='pending'
        )
        
        RequestApprovalService.approve_request(request.id, admin)
        
        # Try to cancel
        with pytest.raises(ValueError, match="cannot be cancelled"):
            RequestApprovalService.cancel_request(request.id, user)
    
    def test_only_requester_can_cancel(self):
        """Test only requester can cancel their own request"""
        company = Company.objects.create(name="Test Company")
        user1 = User.objects.create_user(
            username="user1_test",
            role="user1",
            company=company
        )
        user2 = User.objects.create_user(
            username="user2_test",
            role="user1",
            company=company
        )
        
        # Create request by user1
        request = AccessRequest.objects.create(
            requester=user1,
            ep_no="EMP001",
            company=company,
            access_type='permanent',
            justification="Test",
            status='pending'
        )
        
        # Try to cancel by user2
        with pytest.raises(ValueError, match="Only the requester"):
            RequestApprovalService.cancel_request(request.id, user2)
