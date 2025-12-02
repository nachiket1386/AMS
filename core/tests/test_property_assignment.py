"""
Property-based tests for EmployeeAssignment model
Feature: user1-supervisor-management
"""
import pytest
from hypothesis import given, strategies as st, settings
from datetime import date, timedelta
from django.utils import timezone
from core.models import EmployeeAssignment, User, Company


@pytest.mark.django_db(transaction=True)
class TestEmployeeAssignmentProperties:
    """Property-based tests for EmployeeAssignment"""
    
    @settings(max_examples=100, deadline=None)
    @given(
        days_offset=st.integers(min_value=-365, max_value=365)
    )
    def test_property_17_automatic_assignment_expiration(self, days_offset):
        """
        Feature: user1-supervisor-management, Property 17: Automatic Assignment Expiration
        Validates: Requirements 6.4
        
        For any employee assignment with an end date in the past, 
        the assignment should not be active.
        """
        # Create test data (use get_or_create to avoid unique constraint errors)
        company, _ = Company.objects.get_or_create(name="Test Company")
        
        # Create unique users for each test run
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        user, _ = User.objects.get_or_create(
            username=f"testuser1_{unique_id}",
            defaults={'role': 'user1', 'company': company}
        )
        admin, _ = User.objects.get_or_create(
            username=f"admin1_{unique_id}",
            defaults={'role': 'admin', 'company': company}
        )
        
        # Create assignment with end date relative to today
        today = timezone.now().date()
        end_date = today + timedelta(days=days_offset)
        
        assignment = EmployeeAssignment.objects.create(
            user=user,
            ep_no="EMP001",
            ep_name="Test Employee",
            company=company,
            access_from=today - timedelta(days=30),
            access_to=end_date,
            assigned_by=admin,
            source="admin",
            is_active=True
        )
        
        # Property: Assignment with past end date should not be active
        is_active_today = assignment.is_active_on_date(today)
        
        if end_date < today:
            # Past end date - should not be active
            assert not is_active_today, \
                f"Assignment with end_date {end_date} (past) should not be active on {today}"
        else:
            # Future or today end date - should be active
            assert is_active_today, \
                f"Assignment with end_date {end_date} (future/today) should be active on {today}"



@pytest.mark.django_db(transaction=True)
class TestAccessControlProperties:
    """Property-based tests for AccessControlService"""
    
    @settings(max_examples=100, deadline=None)
    @given(
        num_assigned=st.integers(min_value=0, max_value=5),
        num_unassigned=st.integers(min_value=0, max_value=5)
    )
    def test_property_1_access_control_filtering(self, num_assigned, num_unassigned):
        """
        Feature: user1-supervisor-management, Property 1: Access Control Filtering
        Validates: Requirements 1.1, 1.2, 1.3, 1.5
        
        For any User1 user and any operation (view, search, export, statistics),
        all returned attendance records should belong only to employees assigned to that User1 user.
        """
        from core.models import AttendanceRecord
        from core.services.access_control_service import AccessControlService
        
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
        
        # Create assignments and attendance records for assigned employees
        assigned_ep_nos = []
        for i in range(num_assigned):
            ep_no = f"EMP_ASSIGNED_{unique_id}_{i}"
            assigned_ep_nos.append(ep_no)
            
            # Create assignment
            EmployeeAssignment.objects.create(
                user=user,
                ep_no=ep_no,
                ep_name=f"Assigned Employee {i}",
                company=company,
                assigned_by=admin,
                source="admin",
                is_active=True
            )
            
            # Create attendance record
            AttendanceRecord.objects.create(
                ep_no=ep_no,
                ep_name=f"Assigned Employee {i}",
                company=company,
                date=today,
                shift="09:00-17:00",
                overstay="00:00",
                status="P"
            )
        
        # Create attendance records for unassigned employees
        unassigned_ep_nos = []
        for i in range(num_unassigned):
            ep_no = f"EMP_UNASSIGNED_{unique_id}_{i}"
            unassigned_ep_nos.append(ep_no)
            
            AttendanceRecord.objects.create(
                ep_no=ep_no,
                ep_name=f"Unassigned Employee {i}",
                company=company,
                date=today,
                shift="09:00-17:00",
                overstay="00:00",
                status="P"
            )
        
        # Test: Filter queryset by access
        all_records = AttendanceRecord.objects.filter(company=company)
        filtered_records = AccessControlService.filter_queryset_by_access(all_records, user, today)
        
        # Property: All filtered records should belong to assigned employees only
        for record in filtered_records:
            assert record.ep_no in assigned_ep_nos, \
                f"Record {record.ep_no} should be in assigned list {assigned_ep_nos}"
            assert record.ep_no not in unassigned_ep_nos, \
                f"Record {record.ep_no} should not be in unassigned list"
        
        # Property: Count should match number of assigned employees
        assert filtered_records.count() == num_assigned, \
            f"Expected {num_assigned} records, got {filtered_records.count()}"

    
    @settings(max_examples=100, deadline=None)
    @given(
        assignment_type=st.sampled_from(['permanent', 'past', 'current', 'future']),
        query_offset=st.integers(min_value=-60, max_value=60)
    )
    def test_property_19_date_range_access_filtering(self, assignment_type, query_offset):
        """
        Feature: user1-supervisor-management, Property 19: Date Range Access Filtering
        Validates: Requirements 7.1, 7.4, 7.5
        
        For any User1 with date-range assignment and any query date,
        employee data should be visible if and only if the query date falls within
        the assignment's date range (or assignment is permanent).
        """
        from core.services.access_control_service import AccessControlService
        
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
        
        # Create assignment based on type
        if assignment_type == 'permanent':
            access_from = None
            access_to = None
        elif assignment_type == 'past':
            access_from = today - timedelta(days=60)
            access_to = today - timedelta(days=30)
        elif assignment_type == 'current':
            access_from = today - timedelta(days=30)
            access_to = today + timedelta(days=30)
        else:  # future
            access_from = today + timedelta(days=30)
            access_to = today + timedelta(days=60)
        
        assignment = EmployeeAssignment.objects.create(
            user=user,
            ep_no=ep_no,
            ep_name="Test Employee",
            company=company,
            access_from=access_from,
            access_to=access_to,
            assigned_by=admin,
            source="admin",
            is_active=True
        )
        
        # Query date
        query_date = today + timedelta(days=query_offset)
        
        # Check access
        has_access = AccessControlService.check_employee_access(user, ep_no, query_date)
        
        # Determine expected access
        should_have_access = False
        if assignment_type == 'permanent':
            should_have_access = True
        elif assignment_type == 'past':
            should_have_access = (access_from <= query_date <= access_to)
        elif assignment_type == 'current':
            should_have_access = (access_from <= query_date <= access_to)
        elif assignment_type == 'future':
            should_have_access = (access_from <= query_date <= access_to)
        
        # Property: Access should match expected
        assert has_access == should_have_access, \
            f"Assignment type={assignment_type}, query_date={query_date}, " \
            f"range=[{access_from}, {access_to}], expected={should_have_access}, got={has_access}"
