"""
Property-based tests for BackupService
Feature: data-backup-sync
"""
from hypothesis import given, settings, strategies as st
from hypothesis.extra.django import TestCase
from django.utils import timezone
from datetime import timedelta
from core.models import Company, AttendanceRecord
from core.services.backup_service import BackupService


class BackupServicePropertyTests(TestCase):
    """Property-based tests for BackupService"""
    
    @settings(max_examples=100)
    @given(
        company_count=st.integers(min_value=0, max_value=10),
        record_count=st.integers(min_value=0, max_value=50)
    )
    def test_backup_completeness(self, company_count, record_count):
        """
        Feature: data-backup-sync, Property 2: Backup completeness
        
        For any database state, when a full backup is created, the backup file 
        should contain exactly the same number of companies and attendance records 
        as exist in the database at that moment.
        
        Validates: Requirements 2.1, 2.2
        """
        # Clear existing data
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Create random companies
        companies = []
        for i in range(company_count):
            company = Company.objects.create(name=f"TestCompany_{i}_{timezone.now().timestamp()}")
            companies.append(company)
        
        # Create random attendance records
        if companies and record_count > 0:
            for i in range(record_count):
                company = companies[i % len(companies)]
                AttendanceRecord.objects.create(
                    ep_no=f"EMP{i:04d}",
                    ep_name=f"Employee {i}",
                    company=company,
                    date=timezone.now().date() - timedelta(days=i % 365),
                    shift="Day",
                    overstay="0",
                    status="P"
                )
        
        # Get actual counts from database
        db_company_count = Company.objects.count()
        db_record_count = AttendanceRecord.objects.count()
        
        # Create backup
        service = BackupService()
        result = service.create_backup(backup_type='full')
        
        # Verify backup was successful
        assert result['success'] is True, f"Backup failed: {result.get('error', 'Unknown error')}"
        
        # Verify counts match
        assert result['companies_count'] == db_company_count, \
            f"Company count mismatch: backup has {result['companies_count']}, database has {db_company_count}"
        assert result['records_count'] == db_record_count, \
            f"Record count mismatch: backup has {result['records_count']}, database has {db_record_count}"
        
        # Verify data structure
        backup_data = result['data']
        assert len(backup_data['companies']) == db_company_count
        assert len(backup_data['attendance_records']) == db_record_count
    
    @settings(max_examples=100)
    @given(
        company_count=st.integers(min_value=1, max_value=5),
        record_count=st.integers(min_value=1, max_value=20)
    )
    def test_backup_metadata_accuracy(self, company_count, record_count):
        """
        Feature: data-backup-sync, Property 3: Backup metadata accuracy
        
        For any backup file created, the metadata section should accurately reflect 
        the counts of companies and attendance records contained in the backup data section.
        
        Validates: Requirements 2.3
        """
        # Clear existing data
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Create test data
        companies = []
        for i in range(company_count):
            company = Company.objects.create(name=f"MetaTestCo_{i}_{timezone.now().timestamp()}")
            companies.append(company)
        
        for i in range(record_count):
            company = companies[i % len(companies)]
            AttendanceRecord.objects.create(
                ep_no=f"META{i:04d}",
                ep_name=f"Meta Employee {i}",
                company=company,
                date=timezone.now().date(),
                shift="Day",
                overstay="0",
                status="P"
            )
        
        # Create backup
        service = BackupService()
        result = service.create_backup(backup_type='full')
        
        assert result['success'] is True
        
        # Get metadata and actual data
        metadata = result['data']['metadata']
        companies_data = result['data']['companies']
        records_data = result['data']['attendance_records']
        
        # Verify metadata matches actual data
        assert metadata['total_companies'] == len(companies_data), \
            f"Metadata company count {metadata['total_companies']} doesn't match data {len(companies_data)}"
        assert metadata['total_attendance_records'] == len(records_data), \
            f"Metadata record count {metadata['total_attendance_records']} doesn't match data {len(records_data)}"
        
        # Verify metadata has required fields
        assert 'version' in metadata
        assert 'created_at' in metadata
        assert 'backup_type' in metadata
        assert metadata['backup_type'] == 'full'
    
    @settings(max_examples=100)
    @given(
        ep_no=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
        ep_name=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Zs'))),
        status=st.sampled_from(['P', 'A', 'PH', 'WO', '-0.5', '-1'])
    )
    def test_checksum_consistency(self, ep_no, ep_name, status):
        """
        Feature: data-backup-sync, Property 4: Checksum consistency
        
        For any record in a backup file, if the record data has not changed, 
        generating a new checksum for that record should produce the same checksum value.
        
        Validates: Requirements 2.4
        """
        # Clear existing data
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Create a company and record
        company = Company.objects.create(name=f"ChecksumTest_{timezone.now().timestamp()}")
        record = AttendanceRecord.objects.create(
            ep_no=ep_no[:20],  # Limit length
            ep_name=ep_name[:50].strip() or "Test",  # Ensure not empty
            company=company,
            date=timezone.now().date(),
            shift="Day",
            overstay="0",
            status=status
        )
        
        # Create backup twice
        service = BackupService()
        result1 = service.create_backup(backup_type='full')
        result2 = service.create_backup(backup_type='full')
        
        assert result1['success'] is True
        assert result2['success'] is True
        
        # Get the attendance records from both backups
        records1 = result1['data']['attendance_records']
        records2 = result2['data']['attendance_records']
        
        assert len(records1) > 0, "No records in first backup"
        assert len(records2) > 0, "No records in second backup"
        
        # Find matching records by unique key
        record1 = records1[0]
        record2 = records2[0]
        
        # Verify checksums are identical
        assert record1['checksum'] == record2['checksum'], \
            f"Checksums differ for identical record: {record1['checksum']} != {record2['checksum']}"
        
        # Verify checksum is not empty
        assert record1['checksum'], "Checksum is empty"
        assert len(record1['checksum']) == 64, f"Checksum should be 64 chars (SHA256), got {len(record1['checksum'])}"
    
    @settings(max_examples=100)
    @given(
        old_record_count=st.integers(min_value=1, max_value=10),
        new_record_count=st.integers(min_value=1, max_value=10),
        days_ago=st.integers(min_value=1, max_value=30)
    )
    def test_incremental_backup_filtering(self, old_record_count, new_record_count, days_ago):
        """
        Feature: data-backup-sync, Property 12: Incremental backup filtering
        
        For any incremental backup created with a since_date parameter, all records 
        in the backup should have an updated_at timestamp greater than or equal to since_date.
        
        Validates: Requirements 6.2
        """
        # Clear existing data
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Create a company
        company = Company.objects.create(name=f"IncrementalTest_{timezone.now().timestamp()}")
        
        # Create old records (before cutoff date)
        cutoff_date = timezone.now() - timedelta(days=days_ago)
        old_date = cutoff_date - timedelta(days=5)
        
        for i in range(old_record_count):
            record = AttendanceRecord.objects.create(
                ep_no=f"OLD{i:04d}",
                ep_name=f"Old Employee {i}",
                company=company,
                date=old_date.date(),
                shift="Day",
                overstay="0",
                status="P"
            )
            # Manually set updated_at to old date
            AttendanceRecord.objects.filter(pk=record.pk).update(updated_at=old_date)
        
        # Create new records (after cutoff date)
        new_date = cutoff_date + timedelta(days=1)
        
        for i in range(new_record_count):
            record = AttendanceRecord.objects.create(
                ep_no=f"NEW{i:04d}",
                ep_name=f"New Employee {i}",
                company=company,
                date=new_date.date(),
                shift="Day",
                overstay="0",
                status="P"
            )
            # Manually set updated_at to new date
            AttendanceRecord.objects.filter(pk=record.pk).update(updated_at=new_date)
        
        # Create incremental backup
        service = BackupService()
        result = service.create_incremental_backup(since_date=cutoff_date)
        
        assert result['success'] is True, f"Backup failed: {result.get('error', 'Unknown error')}"
        
        # Verify only new records are in backup
        backup_records = result['data']['attendance_records']
        
        # All records in backup should be new records
        assert len(backup_records) == new_record_count, \
            f"Expected {new_record_count} records in incremental backup, got {len(backup_records)}"
        
        # Verify all records have updated_at >= cutoff_date
        for record in backup_records:
            updated_at_str = record['updated_at']
            if updated_at_str:
                from dateutil import parser
                updated_at = parser.parse(updated_at_str)
                assert updated_at >= cutoff_date, \
                    f"Record {record['ep_no']} has updated_at {updated_at} before cutoff {cutoff_date}"
        
        # Verify metadata indicates incremental backup
        metadata = result['data']['metadata']
        assert metadata['backup_type'] == 'incremental'
        assert 'since_date' in metadata
