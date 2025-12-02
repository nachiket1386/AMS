"""
Property-based tests for bulk request processing
Feature: user1-supervisor-management
"""
import pytest
from hypothesis import given, strategies as st, settings, assume
from core.models import User, Company
from core.services.request_approval_service import RequestApprovalService


@pytest.mark.django_db(transaction=True)
class TestBulkRequestProperties:
    """Property-based tests for bulk request processing"""
    
    @settings(max_examples=100, deadline=None)
    @given(
        num_ep_nos=st.integers(min_value=1, max_value=10),
        separator=st.sampled_from([',', '\n', ', '])
    )
    def test_property_20_bulk_request_parsing(self, num_ep_nos, separator):
        """
        Feature: user1-supervisor-management, Property 20: Bulk Request Parsing
        Validates: Requirements 8.1
        
        For any bulk access request with N EP NOs (comma-separated or line-by-line),
        the system should parse exactly N distinct EP NOs.
        """
        # Generate EP NOs
        ep_nos = [f"EMP{i:03d}" for i in range(num_ep_nos)]
        
        # Create input string
        ep_nos_input = separator.join(ep_nos)
        
        # Parse
        valid, invalid = RequestApprovalService.parse_bulk_ep_nos(ep_nos_input)
        
        # Property: Should parse exactly N distinct EP NOs
        assert len(valid) == num_ep_nos, \
            f"Expected {num_ep_nos} EP NOs, got {len(valid)}"
        assert len(invalid) == 0
        assert set(valid) == set(ep_nos)
    
    @settings(max_examples=100, deadline=None)
    @given(
        num_ep_nos=st.integers(min_value=1, max_value=5),
        access_type=st.sampled_from(['date_range', 'permanent'])
    )
    def test_property_21_bulk_request_consistency(self, num_ep_nos, access_type):
        """
        Feature: user1-supervisor-management, Property 21: Bulk Request Consistency
        Validates: Requirements 8.2
        
        For any bulk access request with multiple EP NOs, all created individual requests
        should have identical access type, date range, and justification.
        """
        from datetime import timedelta
        from django.utils import timezone
        
        # Create test data
        company, _ = Company.objects.get_or_create(name="Test Company")
        
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        user, _ = User.objects.get_or_create(
            username=f"user1_{unique_id}",
            defaults={'role': 'user1', 'company': company}
        )
        
        # Generate EP NOs
        ep_nos = [f"EMP_{unique_id}_{i}" for i in range(num_ep_nos)]
        
        # Create dates
        today = timezone.now().date()
        if access_type == 'date_range':
            dates = {
                'access_from': today,
                'access_to': today + timedelta(days=30)
            }
        else:
            dates = {}
        
        justification = "Test bulk request"
        
        # Create bulk request
        requests = RequestApprovalService.create_request(
            user=user,
            ep_nos=ep_nos,
            access_type=access_type,
            dates=dates,
            justification=justification
        )
        
        # Property: All requests should have identical parameters
        assert len(requests) == num_ep_nos
        
        for request in requests:
            assert request.access_type == access_type
            assert request.justification == justification
            
            if access_type == 'date_range':
                assert request.access_from == dates['access_from']
                assert request.access_to == dates['access_to']
            else:
                assert request.access_from is None
                assert request.access_to is None
    
    @settings(max_examples=100, deadline=None)
    @given(
        num_ep_nos=st.integers(min_value=1, max_value=10)
    )
    def test_property_22_bulk_request_splitting(self, num_ep_nos):
        """
        Feature: user1-supervisor-management, Property 22: Bulk Request Splitting
        Validates: Requirements 8.3
        
        For any bulk access request with N EP NOs, exactly N individual access requests
        should be created.
        """
        # Create test data
        company, _ = Company.objects.get_or_create(name="Test Company")
        
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        user, _ = User.objects.get_or_create(
            username=f"user1_{unique_id}",
            defaults={'role': 'user1', 'company': company}
        )
        
        # Generate EP NOs
        ep_nos = [f"EMP_{unique_id}_{i}" for i in range(num_ep_nos)]
        
        # Create bulk request
        requests = RequestApprovalService.create_request(
            user=user,
            ep_nos=ep_nos,
            access_type='permanent',
            dates={},
            justification="Test bulk request"
        )
        
        # Property: Should create exactly N requests
        assert len(requests) == num_ep_nos
        
        # Each EP NO should have its own request
        request_ep_nos = [r.ep_no for r in requests]
        assert set(request_ep_nos) == set(ep_nos)
    
    @settings(max_examples=50, deadline=None)
    @given(
        num_valid=st.integers(min_value=0, max_value=5),
        num_invalid=st.integers(min_value=1, max_value=3)
    )
    def test_property_23_invalid_ep_no_validation(self, num_valid, num_invalid):
        """
        Feature: user1-supervisor-management, Property 23: Invalid EP NO Validation
        Validates: Requirements 8.5
        
        For any bulk access request containing invalid EP NOs, the system should display
        validation errors specifically identifying each invalid EP NO.
        """
        # Generate valid and invalid EP NOs
        valid_ep_nos = [f"EMP{i:03d}" for i in range(num_valid)]
        invalid_ep_nos = ["" for _ in range(num_invalid)]  # Empty strings are invalid
        
        # Mix them
        all_ep_nos = valid_ep_nos + invalid_ep_nos
        ep_nos_input = ",".join(all_ep_nos)
        
        # Parse
        valid, invalid = RequestApprovalService.parse_bulk_ep_nos(ep_nos_input)
        
        # Property: Should identify all invalid EP NOs
        assert len(valid) == num_valid
        assert len(invalid) == num_invalid
