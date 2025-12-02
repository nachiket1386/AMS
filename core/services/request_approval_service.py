"""
Request Approval Service for managing access requests
"""
from django.utils import timezone
from django.db import transaction
from core.models import AccessRequest, EmployeeAssignment, AccessRequestAuditLog


class RequestApprovalService:
    """Service for managing access requests and approvals"""
    
    @staticmethod
    def parse_bulk_ep_nos(ep_nos_input):
        """
        Parse bulk EP NO input (comma-separated or line-by-line)
        
        Args:
            ep_nos_input: String with EP NOs (comma-separated or newline-separated)
            
        Returns:
            tuple: (valid_ep_nos, invalid_ep_nos)
        """
        if isinstance(ep_nos_input, list):
            ep_nos = ep_nos_input
        else:
            # Split by comma or newline
            ep_nos = []
            for line in ep_nos_input.replace(',', '\n').split('\n'):
                ep_no = line.strip()
                # Include empty strings to track them as invalid
                ep_nos.append(ep_no)
        
        # Validate EP NOs (basic validation - non-empty)
        valid_ep_nos = []
        invalid_ep_nos = []
        
        for ep_no in ep_nos:
            if ep_no and len(ep_no) > 0:
                valid_ep_nos.append(ep_no)
            elif ep_no == '':
                # Track empty strings as invalid
                invalid_ep_nos.append(ep_no)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_valid = []
        for ep_no in valid_ep_nos:
            if ep_no not in seen:
                seen.add(ep_no)
                unique_valid.append(ep_no)
        
        return unique_valid, invalid_ep_nos
    
    @staticmethod
    @transaction.atomic
    def create_request(user, ep_nos, access_type, dates, justification):
        """
        Create access request(s)
        
        Args:
            user: User1 who is requesting access
            ep_nos: List of employee numbers or single EP NO
            access_type: 'date_range' or 'permanent'
            dates: Dict with 'access_from' and 'access_to' (for date_range)
            justification: Reason for requesting access
            
        Returns:
            list: List of created AccessRequest objects
        """
        # Ensure ep_nos is a list
        if isinstance(ep_nos, str):
            ep_nos = [ep_nos]
        
        created_requests = []
        
        for ep_no in ep_nos:
            # Create request
            request = AccessRequest.objects.create(
                requester=user,
                ep_no=ep_no.strip(),
                company=user.company,
                access_type=access_type,
                access_from=dates.get('access_from') if access_type == 'date_range' else None,
                access_to=dates.get('access_to') if access_type == 'date_range' else None,
                justification=justification,
                status='pending'
            )
            
            created_requests.append(request)
            
            # Log request creation
            AccessRequestAuditLog.create_log_entry(
                action='request_created',
                actor=user,
                target_user=user,
                target_ep_no=ep_no.strip(),
                details={
                    'request_id': request.id,
                    'access_type': access_type,
                    'justification': justification
                }
            )
        
        return created_requests
    
    @staticmethod
    @transaction.atomic
    def approve_request(request_id, admin_user):
        """
        Approve request and create assignment
        
        Args:
            request_id: ID of the AccessRequest
            admin_user: Admin user approving the request
            
        Returns:
            EmployeeAssignment: Created assignment
            
        Raises:
            ValueError: If request cannot be approved
        """
        try:
            request = AccessRequest.objects.get(id=request_id)
        except AccessRequest.DoesNotExist:
            raise ValueError(f"Request {request_id} not found")
        
        if not request.can_approve():
            raise ValueError(f"Request {request_id} cannot be approved (status: {request.status})")
        
        # Update request status
        request.status = 'approved'
        request.reviewed_by = admin_user
        request.reviewed_at = timezone.now()
        request.save()
        
        # Create employee assignment
        assignment = EmployeeAssignment.objects.create(
            user=request.requester,
            ep_no=request.ep_no,
            ep_name=f"Employee {request.ep_no}",  # Will be updated from actual data
            company=request.company,
            access_from=request.access_from,
            access_to=request.access_to,
            assigned_by=admin_user,
            source='request',
            is_active=True
        )
        
        # Log approval
        AccessRequestAuditLog.create_log_entry(
            action='request_approved',
            actor=admin_user,
            target_user=request.requester,
            target_ep_no=request.ep_no,
            details={
                'request_id': request.id,
                'assignment_id': assignment.id
            }
        )
        
        # Log assignment creation
        AccessRequestAuditLog.create_log_entry(
            action='assignment_created',
            actor=admin_user,
            target_user=request.requester,
            target_ep_no=request.ep_no,
            details={
                'assignment_id': assignment.id,
                'source': 'request',
                'request_id': request.id
            }
        )
        
        return assignment
    
    @staticmethod
    @transaction.atomic
    def reject_request(request_id, admin_user, reason=''):
        """
        Reject request with reason
        
        Args:
            request_id: ID of the AccessRequest
            admin_user: Admin user rejecting the request
            reason: Reason for rejection
            
        Returns:
            AccessRequest: Updated request
            
        Raises:
            ValueError: If request cannot be rejected
        """
        try:
            request = AccessRequest.objects.get(id=request_id)
        except AccessRequest.DoesNotExist:
            raise ValueError(f"Request {request_id} not found")
        
        if not request.can_reject():
            raise ValueError(f"Request {request_id} cannot be rejected (status: {request.status})")
        
        # Update request status
        request.status = 'rejected'
        request.reviewed_by = admin_user
        request.reviewed_at = timezone.now()
        request.rejection_reason = reason
        request.save()
        
        # Log rejection
        AccessRequestAuditLog.create_log_entry(
            action='request_rejected',
            actor=admin_user,
            target_user=request.requester,
            target_ep_no=request.ep_no,
            details={
                'request_id': request.id,
                'reason': reason
            }
        )
        
        return request
    
    @staticmethod
    @transaction.atomic
    def cancel_request(request_id, user):
        """
        Cancel pending request
        
        Args:
            request_id: ID of the AccessRequest
            user: User cancelling the request (must be requester)
            
        Returns:
            AccessRequest: Updated request
            
        Raises:
            ValueError: If request cannot be cancelled
        """
        try:
            request = AccessRequest.objects.get(id=request_id)
        except AccessRequest.DoesNotExist:
            raise ValueError(f"Request {request_id} not found")
        
        if request.requester != user:
            raise ValueError("Only the requester can cancel their own request")
        
        if not request.can_cancel():
            raise ValueError(f"Request {request_id} cannot be cancelled (status: {request.status})")
        
        # Update request status
        request.status = 'cancelled'
        request.save()
        
        # Log cancellation
        AccessRequestAuditLog.create_log_entry(
            action='request_cancelled',
            actor=user,
            target_user=user,
            target_ep_no=request.ep_no,
            details={
                'request_id': request.id
            }
        )
        
        return request
