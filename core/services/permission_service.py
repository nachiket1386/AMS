"""
Permission Service for Excel File Upload Integration

This service handles role-based access control for file uploads and data queries.
"""
from django.db.models import Q
from typing import Optional
import logging

from core.models import User, UploadPermission
from core.services.file_parser_service import FileType

logger = logging.getLogger(__name__)


class PermissionService:
    """Service for managing upload permissions and role-based access"""
    
    def can_upload(self, user: User, file_type: FileType) -> bool:
        """
        Check if user can upload specific file type
        
        Args:
            user: User to check permissions for
            file_type: Type of file to upload
            
        Returns:
            True if user has permission, False otherwise
        """
        if not user or not user.is_authenticated:
            return False
        
        # Root and admin users can upload any file type
        if user.role in ['root', 'admin']:
            return True
        
        # Check specific upload permission for other users
        try:
            permission = UploadPermission.objects.get(
                user=user,
                file_type=file_type.value
            )
            return permission.can_upload
        except UploadPermission.DoesNotExist:
            return False
    
    def get_query_scope(self, user: User) -> Q:
        """
        Return Django Q object for filtering based on role
        
        Args:
            user: User to get scope for
            
        Returns:
            Q object for filtering queries
        """
        if not user or not user.is_authenticated:
            return Q(pk__in=[])  # Return empty queryset
        
        # Root users see everything
        if user.role == 'root':
            return Q()  # No restrictions
        
        # Admin users see data for their company
        if user.role == 'admin':
            if user.company:
                return Q(employee__contractor__contractor_name__icontains=user.company.name)
            return Q()  # No company assigned, see everything
        
        # User1 sees only assigned employees
        if user.role == 'user1':
            from core.models import EmployeeAssignment
            
            # Get assigned employee numbers
            assigned_ep_nos = EmployeeAssignment.objects.filter(
                user=user,
                is_active=True
            ).values_list('ep_no', flat=True)
            
            return Q(employee__ep_no__in=assigned_ep_nos)
        
        # Default: no access
        return Q(pk__in=[])
    
    def filter_queryset(self, queryset, user: User):
        """
        Apply role-based filtering to queryset
        
        Args:
            queryset: QuerySet to filter
            user: User to apply filtering for
            
        Returns:
            Filtered queryset
        """
        scope = self.get_query_scope(user)
        return queryset.filter(scope)
    
    def grant_permission(self, user: User, file_type: str, granted_by: User) -> UploadPermission:
        """
        Grant upload permission to a user
        
        Args:
            user: User to grant permission to
            file_type: Type of file to allow
            granted_by: User granting the permission
            
        Returns:
            UploadPermission object
        """
        permission, created = UploadPermission.objects.update_or_create(
            user=user,
            file_type=file_type,
            defaults={
                'can_upload': True,
                'granted_by': granted_by
            }
        )
        
        action = "granted" if created else "updated"
        logger.info(f"Upload permission {action} for {user.username} - {file_type} by {granted_by.username}")
        
        return permission
    
    def revoke_permission(self, user: User, file_type: str) -> bool:
        """
        Revoke upload permission from a user
        
        Args:
            user: User to revoke permission from
            file_type: Type of file to revoke
            
        Returns:
            True if permission was revoked, False if not found
        """
        try:
            permission = UploadPermission.objects.get(
                user=user,
                file_type=file_type
            )
            permission.can_upload = False
            permission.save()
            
            logger.info(f"Upload permission revoked for {user.username} - {file_type}")
            return True
        except UploadPermission.DoesNotExist:
            return False
    
    def get_user_permissions(self, user: User) -> list:
        """
        Get all upload permissions for a user
        
        Args:
            user: User to get permissions for
            
        Returns:
            List of UploadPermission objects
        """
        return list(UploadPermission.objects.filter(user=user))
    
    def can_view_employee_data(self, user: User, ep_no: str) -> bool:
        """
        Check if user can view specific employee's data
        
        Args:
            user: User to check
            ep_no: Employee number to check access for
            
        Returns:
            True if user has access, False otherwise
        """
        if not user or not user.is_authenticated:
            return False
        
        # Root users can view everything
        if user.role == 'root':
            return True
        
        # Admin users can view employees in their company
        if user.role == 'admin':
            from core.models import Employee
            try:
                employee = Employee.objects.get(ep_no=ep_no)
                if user.company:
                    return user.company.name.lower() in employee.contractor.contractor_name.lower()
                return True
            except Employee.DoesNotExist:
                return False
        
        # User1 can view assigned employees
        if user.role == 'user1':
            from core.models import EmployeeAssignment
            return EmployeeAssignment.objects.filter(
                user=user,
                ep_no=ep_no,
                is_active=True
            ).exists()
        
        return False
    
    def can_view_contractor_data(self, user: User, contractor_code: int) -> bool:
        """
        Check if user can view specific contractor's data
        
        Args:
            user: User to check
            contractor_code: Contractor code to check access for
            
        Returns:
            True if user has access, False otherwise
        """
        if not user or not user.is_authenticated:
            return False
        
        # Root users can view everything
        if user.role == 'root':
            return True
        
        # Admin users can view contractors in their company
        if user.role == 'admin':
            from core.models import Contractor
            try:
                contractor = Contractor.objects.get(contractor_code=contractor_code)
                if user.company:
                    return user.company.name.lower() in contractor.contractor_name.lower()
                return True
            except Contractor.DoesNotExist:
                return False
        
        # User1 can view contractors of assigned employees
        if user.role == 'user1':
            from core.models import EmployeeAssignment, Employee
            assigned_ep_nos = EmployeeAssignment.objects.filter(
                user=user,
                is_active=True
            ).values_list('ep_no', flat=True)
            
            return Employee.objects.filter(
                ep_no__in=assigned_ep_nos,
                contractor__contractor_code=contractor_code
            ).exists()
        
        return False
