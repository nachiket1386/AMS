"""
Property-based tests for ConflictResolver
Feature: data-backup-sync
"""
from hypothesis import given, settings, strategies as st
from hypothesis.extra.django import TestCase
from django.utils import timezone
from datetime import timedelta
from core.models import Company, AttendanceRecord
from core.services.conflict_resolver import ConflictResolver
from core.services.backup_service import BackupService


class ConflictResolverPropertyTests(TestCase):
    """Property-based tests for ConflictResolver"""
    
    @settings(max_examples=100)
    @given(
        ep_no=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
        ep_name=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Zs'))),
        status1=st.sampled_from(['P', 'A', 'PH', 'WO']),
        status2=st.sampled_from(['P', 'A', 'PH', 'WO'])
    )
    def test_checksum_based_change_detection(self, ep_no, ep_name, status1, status2):
        """
        Feature: data-backup-sync, Property 10: Checksum-based change detection
        
        For any two records with the same unique key, if their checksums differ, 
        the records should be detected as having different data.
        
        Validates: Requirements 5.2
        """
        # Create sample records with different statuses
        backup_record = {
            'ep_no': ep_no[:20],
            'ep_name': ep_name[:50].strip() or "Test",
            'company_name': 'Test Company',
            'date': '2025-11-25',
            'shift': 'Day',
            'overstay': '0',
            'status': status1,
            'in_time': None,
            'out_time': None,
            'in_time_2': None,
            'out_time_2': None,
            'in_time_3': None,
            'out_time_3': None,
            'overtime': None,
            'overtime_to_mandays': None,
            'created_at': '2025-11-25T10:00:00',
            'updated_at': '2025-11-25T10:00:00'
        }
        
        db_record = {
            'ep_no': ep_no[:20],
            'ep_name': ep_name[:50].strip() or "Test",
            'company_name': 'Test Company',
            'date': '2025-11-25',
            'shift': 'Day',
            'overstay': '0',
            'status': status2,
            'in_time': None,
            'out_time': None,
            'in_time_2': None,
            'out_time_2': None,
            'in_time_3': None,
            'out_time_3': None,
            'overtime': None,
            'overtime_to_mandays': None,
            'created_at': '2025-11-25T11:00:00',  # Different timestamp
            'updated_at': '2025-11-25T11:00:00'   # Different timestamp
        }
        
        # Generate checksums
        service = BackupService()
        backup_record['checksum'] = service._generate_checksum(backup_record)
        db_record['checksum'] = service._generate_checksum(db_record)
        
        # Use ConflictResolver to detect changes
        resolver = ConflictResolver()
        has_conflict = resolver.detect_conflicts(backup_record, db_record)
        
        if status1 == status2:
            # If status didn't change, no conflict should be detected
            # (timestamps are excluded from comparison)
            assert not has_conflict, \
                f"No conflict expected when status unchanged, but got conflict"
            
            # Verify checksums are the same (since only timestamps differ)
            assert backup_record['checksum'] == db_record['checksum'], \
                f"Checksums should be same when only timestamps differ"
        else:
            # If status changed, conflict should be detected
            has_conflict = resolver.detect_conflicts(backup_record, db_record)
            assert has_conflict, \
                f"Conflict expected when status changed from {status1} to {status2}, but none detected"
            
            # Verify checksums actually differ
            assert backup_record['checksum'] != db_record['checksum'], \
                f"Checksums should differ when data changes"
    
    @settings(max_examples=100)
    @given(
        strategy=st.sampled_from(['backup_wins', 'database_wins']),
        backup_status=st.sampled_from(['P', 'A', 'PH']),
        db_status=st.sampled_from(['P', 'A', 'PH'])
    )
    def test_merge_strategy_application(self, strategy, backup_status, db_status):
        """
        Feature: data-backup-sync, Property (from 5.3): Merge strategy correctness
        
        For any conflict between backup and database records, applying a merge strategy 
        should return the correct record according to the strategy.
        
        Validates: Requirements 5.3
        """
        # Create sample records
        backup_record = {
            'ep_no': 'EMP001',
            'ep_name': 'Test Employee',
            'company_name': 'Test Company',
            'date': '2025-11-25',
            'shift': 'Day',
            'overstay': '0',
            'status': backup_status,
            'checksum': 'backup_checksum_123'
        }
        
        db_record = {
            'ep_no': 'EMP001',
            'ep_name': 'Test Employee',
            'company_name': 'Test Company',
            'date': '2025-11-25',
            'shift': 'Day',
            'overstay': '0',
            'status': db_status,
            'checksum': 'db_checksum_456'
        }
        
        # Apply merge strategy
        resolver = ConflictResolver()
        result = resolver.apply_merge_strategy(backup_record, db_record, strategy)
        
        # Verify correct record is returned
        if strategy == 'backup_wins':
            assert result == backup_record, \
                f"backup_wins strategy should return backup record"
            assert result['status'] == backup_status
            assert result['checksum'] == 'backup_checksum_123'
        elif strategy == 'database_wins':
            assert result == db_record, \
                f"database_wins strategy should return database record"
            assert result['status'] == db_status
            assert result['checksum'] == 'db_checksum_456'
    
    @settings(max_examples=100)
    @given(
        ep_no=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
        shift1=st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=('Lu', 'Ll'))),
        shift2=st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=('Lu', 'Ll')))
    )
    def test_records_differ_detection(self, ep_no, shift1, shift2):
        """
        Test that _records_differ correctly identifies when records have different data
        """
        record1 = {
            'ep_no': ep_no[:20],
            'ep_name': 'Test Employee',
            'company_name': 'Test Company',
            'date': '2025-11-25',
            'shift': shift1[:10],
            'status': 'P',
            'created_at': '2025-11-25T10:00:00',
            'updated_at': '2025-11-25T10:00:00'
        }
        
        record2 = {
            'ep_no': ep_no[:20],
            'ep_name': 'Test Employee',
            'company_name': 'Test Company',
            'date': '2025-11-25',
            'shift': shift2[:10],
            'status': 'P',
            'created_at': '2025-11-25T11:00:00',  # Different timestamp
            'updated_at': '2025-11-25T11:00:00'   # Different timestamp
        }
        
        resolver = ConflictResolver()
        differs = resolver._records_differ(record1, record2)
        
        if shift1 == shift2:
            # Records should be considered identical (timestamps excluded)
            assert not differs, \
                f"Records should be identical when only timestamps differ"
        else:
            # Records should be different
            assert differs, \
                f"Records should differ when shift changes from '{shift1}' to '{shift2}'"
