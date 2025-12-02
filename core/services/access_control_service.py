"""
Access Control Service for User1 supervisor management
"""
from django.utils import timezone
from django.db.models import Q
from core.models import EmployeeAssignment, User


class AccessControlService:
    """Service for checking and filtering employee access for User1 users"""
    
    @staticmethod
    def check_employee_access(user, ep_no, date=None):
        """
        Check if user has access to employee on specific date
        
        Args:
            user: User object (should be User1)
            ep_no: Employee number to check
            date: Date to check (defaults to today)
            
        Returns:
            bool: True if user has access to employee on the given date
        """
        if date is None:
            date = timezone.now().date()
        
        # Root and Admin have access to all employees
        if user.role in ['root', 'admin']:
            return True
        
        # User1 must have an active assignment
        if user.role == 'user1':
            assignments = EmployeeAssignment.objects.filter(
                user=user,
                ep_no=ep_no,
                is_active=True
            )
            
            for assignment in assignments:
                if assignment.is_active_on_date(date):
                    return True
        
        return False
    
    @staticmethod
    def get_assigned_employees(user, date=None):
        """
        Get list of EP NOs user can access
        
        Args:
            user: User object
            date: Date to check (defaults to today)
            
        Returns:
            list: List of EP NOs the user can access
        """
        if date is None:
            date = timezone.now().date()
        
        # Root and Admin have access to all employees (return None to indicate "all")
        if user.role in ['root', 'admin']:
            return None
        
        # User1 - get assigned employees
        if user.role == 'user1':
            assignments = EmployeeAssignment.objects.filter(
                user=user,
                is_active=True
            )
            
            ep_nos = []
            for assignment in assignments:
                if assignment.is_active_on_date(date):
                    ep_nos.append(assignment.ep_no)
            
            return ep_nos
        
        return []
    
    @staticmethod
    def filter_queryset_by_access(queryset, user, date=None):
        """
        Filter attendance queryset by user's assignments
        
        Args:
            queryset: AttendanceRecord queryset
            user: User object
            date: Date to check (defaults to today)
            
        Returns:
            queryset: Filtered queryset
        """
        if date is None:
            date = timezone.now().date()
        
        # Root and Admin see all records
        if user.role in ['root', 'admin']:
            return queryset
        
        # User1 - filter by assigned employees
        if user.role == 'user1':
            ep_nos = AccessControlService.get_assigned_employees(user, date)
            if ep_nos is None:
                # Should not happen for User1, but handle gracefully
                return queryset
            elif len(ep_nos) == 0:
                # No assignments - return empty queryset
                return queryset.none()
            else:
                # Filter by assigned EP NOs
                return queryset.filter(ep_no__in=ep_nos)
        
        # Unknown role - return empty queryset
        return queryset.none()
    
    @staticmethod
    def is_assignment_active(assignment, check_date=None):
        """
        Check if assignment is currently active
        
        Args:
            assignment: EmployeeAssignment object
            check_date: Date to check (defaults to today)
            
        Returns:
            bool: True if assignment is active on the given date
        """
        if check_date is None:
            check_date = timezone.now().date()
        
        return assignment.is_active_on_date(check_date)
