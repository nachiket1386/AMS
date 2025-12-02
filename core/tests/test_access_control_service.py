"""
Unit tests for AccessControlService
"""
import pytest
from datetime import timedelta
from django.utils import timezone
from core.models import EmployeeAssignment, User, Company, AttendanceRecord
from core.services.access_control_service import AccessControlService


@pytest.mark.django_db
class TestAccessControlService:
    """Unit tests for AccessControlService"""
    
    def test_user1_with_no_assignments_sees_empty_list(self):
        """Test User1 with no assignments sees empty list"""
        company = Company.objects.create(name="Test Company")
        user = User.objects.create_user(
            username="user1_test",
            role="user1",
            company=company
        )
        
        # Create some attendance records
        AttendanceRecord.objects.create(
            ep_no="EMP001",
            ep_name="Employee 1",
            company=company,
            date=timezone.now().date(),
            shift="09:00-17:00",
            overstay="00:00",
            status="P"
        )
        
        # Get assigned employees
        ep_nos = AccessControlService.get_assigned_employees(user)
        
        # Should return empty list
        assert ep_nos == []
        
        # Filter queryset should return empty
        all_records = AttendanceRecord.objects.all()
        filtered = AccessControlService.filter_queryset_by_access(all_records, user)
        assert filtered.count() == 0
    
    def test_expired_assignment_does_not_grant_access(self):
        """Test expired assignment does not grant access"""
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
        
        today = timezone.now().date()
        
        # Create expired assignment (ended yesterday)
        assignment = EmployeeAssignment.objects.create(
            user=user,
            ep_no="EMP001",
            ep_name="Employee 1",
            company=company,
            access_from=today - timedelta(days=30),
            access_to=today - timedelta(days=1),
            assigned_by=admin,
            source="admin",
            is_active=True
        )
        
        # Check access today
        has_access = AccessControlService.check_employee_access(user, "EMP001", today)
        
        # Should not have access
        assert not has_access
    
    def test_future_assignment_does_not_grant_current_access(self):
        """Test future assignment does not grant current access"""
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
        
        today = timezone.now().date()
        
        # Create future assignment (starts tomorrow)
        assignment = EmployeeAssignment.objects.create(
            user=user,
            ep_no="EMP001",
            ep_name="Employee 1",
            company=company,
            access_from=today + timedelta(days=1),
            access_to=today + timedelta(days=30),
            assigned_by=admin,
            source="admin",
            is_active=True
        )
        
        # Check access today
        has_access = AccessControlService.check_employee_access(user, "EMP001", today)
        
        # Should not have access
        assert not has_access
    
    def test_admin_has_access_to_all(self):
        """Test Admin users have access to all employees"""
        company = Company.objects.create(name="Test Company")
        admin = User.objects.create_user(
            username="admin_test",
            role="admin",
            company=company
        )
        
        # Check access without any assignments
        has_access = AccessControlService.check_employee_access(admin, "EMP001")
        assert has_access
        
        # Get assigned employees should return None (all)
        ep_nos = AccessControlService.get_assigned_employees(admin)
        assert ep_nos is None
    
    def test_root_has_access_to_all(self):
        """Test Root users have access to all employees"""
        root = User.objects.create_user(
            username="root_test",
            role="root"
        )
        
        # Check access without any assignments
        has_access = AccessControlService.check_employee_access(root, "EMP001")
        assert has_access
        
        # Get assigned employees should return None (all)
        ep_nos = AccessControlService.get_assigned_employees(root)
        assert ep_nos is None
