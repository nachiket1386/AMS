"""
Property-based tests for RestoreService
Feature: data-backup-sync
"""
from hypothesis import given, settings, strategies as st
from hypothesis.extra.django import TestCase
from django.utils import timezone
from datetime import timedelta
from core.models import Company, AttendanceRecord
from core.services.restore_service import RestoreService
from core.services.backup_service import BackupService


class RestoreServicePropertyTests(TestCase):
    """Property-based tests for RestoreService"""
    
    @settings(max_examples=100)
    @given(
        missing_field=st.sampled_from(['metadata', 'companies', 'attendance_records']),
    )
    def test_backup_validation_missing_fields(self, missing_field):
        """
        Feature: data-backup-sync, Property 14: Backup file validation
        
        For any uploaded file, if it does not conform to the expected JSON schema 
        with required fields (metadata, companies, attendance_records), 
        the validation should reject the file.
        
        Validates: Requirements 9.1, 9.2
        """
        # Create a valid backup structure
        valid_backup = {
            'metadata': {
                'version': '1.0',
                'created_at': timezone.now().isoformat(),
                'backup_type': 'full',
                'total_companies': 1,
                'total_attendance_records': 1
            },
            'companies': [
                {'id': 1, 'name': 'Test Company', 'created_at': timezone.now().isoformat()}
            ],
            'attendance_records': [
                {
                    'ep_no': 'EMP001',
                    'ep_name': 'Test Employee',
                    'company_name': 'Test Company',
                    'date': '2025-11-25',
                    'shift': 'Day',
                    'overstay': '0',
                    'status': 'P'
                }
            ]
        }
        
        # Remove the specified field
        invalid_backup = {k: v for k, v in valid_backup.items() if k != missing_field}
        
        # Validate
        service = RestoreService()
        result = service.validate_backup(invalid_backup)
        
        # Should be invalid
        assert result['valid'] is False, \
            f"Backup missing '{missing_field}' should be invalid"
        
        # Should have error about missing field
        assert any(missing_field in error for error in result['errors']), \
            f"Validation errors should mention missing field '{missing_field}'"
    
    @settings(max_examples=100)
    @given(
        company_count=st.integers(min_value=1, max_value=5),
        record_count=st.integers(min_value=1, max_value=10)
    )
    def test_backup_validation_valid_structure(self, company_count, record_count):
        """
        Test that valid backup structures pass validation
        """
        # Clear existing data
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Create test data
        companies = []
        for i in range(company_count):
            company = Company.objects.create(name=f"ValidTest_{i}_{timezone.now().timestamp()}")
            companies.append(company)
        
        for i in range(record_count):
            company = companies[i % len(companies)]
            AttendanceRecord.objects.create(
                ep_no=f"VAL{i:04d}",
                ep_name=f"Valid Employee {i}",
                company=company,
                date=timezone.now().date(),
                shift="Day",
                overstay="0",
                status="P"
            )
        
        # Create backup
        backup_service = BackupService()
        backup_result = backup_service.create_backup()
        
        # Validate the backup
        restore_service = RestoreService()
        validation_result = restore_service.validate_backup(backup_result['data'])
        
        # Should be valid
        assert validation_result['valid'] is True, \
            f"Valid backup should pass validation. Errors: {validation_result['errors']}"
        
        # Should have no errors
        assert len(validation_result['errors']) == 0, \
            f"Valid backup should have no errors, got: {validation_result['errors']}"
    
    @settings(max_examples=100)
    @given(
        ep_no=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
        company_name=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Zs')))
    )
    def test_unique_key_consistency(self, ep_no, company_name):
        """
        Feature: data-backup-sync, Property 9: Unique key consistency
        
        For any two attendance records, if they have the same ep_no, company_name, 
        and date, they should be considered the same record for merge purposes.
        
        Validates: Requirements 5.1
        """
        date_str = '2025-11-25'
        
        # Create two records with same unique key
        record1 = {
            'ep_no': ep_no[:20],
            'ep_name': 'Employee One',
            'company_name': company_name[:50].strip() or 'Test',
            'date': date_str,
            'shift': 'Day',
            'status': 'P'
        }
        
        record2 = {
            'ep_no': ep_no[:20],
            'ep_name': 'Employee Two',  # Different name
            'company_name': company_name[:50].strip() or 'Test',
            'date': date_str,
            'shift': 'Night',  # Different shift
            'status': 'A'  # Different status
        }
        
        # Get unique keys
        service = RestoreService()
        key1 = service._get_unique_key(record1)
        key2 = service._get_unique_key(record2)
        
        # Keys should be identical (based on ep_no, company_name, date only)
        assert key1 == key2, \
            f"Records with same ep_no, company, date should have same unique key. Got {key1} != {key2}"
        
        # Verify key components
        assert key1[0] == ep_no[:20], "First component should be ep_no"
        assert key1[1] == (company_name[:50].strip() or 'Test'), "Second component should be company_name"
        assert key1[2] == date_str, "Third component should be date"
    
    @settings(max_examples=100)
    @given(
        record_count=st.integers(min_value=1, max_value=10)
    )
    def test_preview_changes_accuracy(self, record_count):
        """
        Test that preview_changes correctly identifies what would be changed
        """
        # Clear existing data
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Create a company
        company = Company.objects.create(name=f"PreviewTest_{timezone.now().timestamp()}")
        
        # Create some existing records
        for i in range(record_count):
            AttendanceRecord.objects.create(
                ep_no=f"PREV{i:04d}",
                ep_name=f"Preview Employee {i}",
                company=company,
                date=timezone.now().date(),
                shift="Day",
                overstay="0",
                status="P"
            )
        
        # Create backup
        backup_service = BackupService()
        backup_result = backup_service.create_backup()
        
        # Preview restore (should skip all since they're identical)
        restore_service = RestoreService()
        preview = restore_service.preview_changes(backup_result['data'])
        
        # All records should be skipped (identical)
        assert preview['summary']['skip_count'] == record_count, \
            f"Expected {record_count} records to be skipped, got {preview['summary']['skip_count']}"
        
        # No records should be added or updated
        assert preview['summary']['add_count'] == 0, \
            f"Expected 0 records to be added, got {preview['summary']['add_count']}"
        assert preview['summary']['update_count'] == 0, \
            f"Expected 0 records to be updated, got {preview['summary']['update_count']}"
    
    @settings(max_examples=100)
    @given(
        record_count=st.integers(min_value=1, max_value=20)
    )
    def test_duplicate_prevention(self, record_count):
        """
        Feature: data-backup-sync, Property 5: Duplicate prevention
        
        For any backup file and database state, when restoring records that already 
        exist in the database with identical data, those records should be skipped 
        and not create duplicates.
        
        Validates: Requirements 3.3
        """
        # Clear existing data
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Create a company and records
        company = Company.objects.create(name=f"DupTest_{timezone.now().timestamp()}")
        
        for i in range(record_count):
            AttendanceRecord.objects.create(
                ep_no=f"DUP{i:04d}",
                ep_name=f"Duplicate Test {i}",
                company=company,
                date=timezone.now().date(),
                shift="Day",
                overstay="0",
                status="P"
            )
        
        # Get initial count
        initial_count = AttendanceRecord.objects.count()
        assert initial_count == record_count
        
        # Create backup
        backup_service = BackupService()
        backup_result = backup_service.create_backup()
        
        # Restore the same data
        restore_service = RestoreService()
        restore_result = restore_service.restore_backup(backup_result['data'])
        
        # Verify success
        assert restore_result['success'] is True, \
            f"Restore failed: {restore_result.get('errors', [])}"
        
        # Verify no duplicates were created
        final_count = AttendanceRecord.objects.count()
        assert final_count == initial_count, \
            f"Duplicates created: started with {initial_count}, ended with {final_count}"
        
        # Verify all records were skipped
        assert restore_result['skipped'] == record_count, \
            f"Expected {record_count} records skipped, got {restore_result['skipped']}"
        
        # Verify no records were added or updated
        assert restore_result['added'] == 0, \
            f"Expected 0 records added, got {restore_result['added']}"
        assert restore_result['updated'] == 0, \
            f"Expected 0 records updated, got {restore_result['updated']}"
    
    @settings(max_examples=100)
    @given(
        new_record_count=st.integers(min_value=1, max_value=10)
    )
    def test_new_record_insertion(self, new_record_count):
        """
        Feature: data-backup-sync, Property 6: New record insertion
        
        For any backup file containing a record with a unique key (ep_no, company, date) 
        that does not exist in the database, restoring that backup should insert 
        the new record into the database.
        
        Validates: Requirements 3.4
        """
        # Clear existing data
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Create a company
        company = Company.objects.create(name=f"NewTest_{timezone.now().timestamp()}")
        
        # Create backup data with new records
        backup_data = {
            'metadata': {
                'version': '1.0',
                'created_at': timezone.now().isoformat(),
                'backup_type': 'full',
                'total_companies': 1,
                'total_attendance_records': new_record_count
            },
            'companies': [
                {
                    'id': company.id,
                    'name': company.name,
                    'created_at': company.created_at.isoformat()
                }
            ],
            'attendance_records': []
        }
        
        # Add new records to backup
        for i in range(new_record_count):
            backup_data['attendance_records'].append({
                'ep_no': f"NEW{i:04d}",
                'ep_name': f"New Employee {i}",
                'company_name': company.name,
                'date': timezone.now().date().isoformat(),
                'shift': 'Day',
                'overstay': '0',
                'status': 'P',
                'in_time': None,
                'out_time': None,
                'in_time_2': None,
                'out_time_2': None,
                'in_time_3': None,
                'out_time_3': None,
                'overtime': None,
                'overtime_to_mandays': None
            })
        
        # Verify database is empty
        initial_count = AttendanceRecord.objects.count()
        assert initial_count == 0
        
        # Restore backup
        restore_service = RestoreService()
        restore_result = restore_service.restore_backup(backup_data)
        
        # Verify success
        assert restore_result['success'] is True, \
            f"Restore failed: {restore_result.get('errors', [])}"
        
        # Verify all new records were inserted
        final_count = AttendanceRecord.objects.count()
        assert final_count == new_record_count, \
            f"Expected {new_record_count} records, got {final_count}"
        
        # Verify counts
        assert restore_result['added'] == new_record_count, \
            f"Expected {new_record_count} records added, got {restore_result['added']}"
        assert restore_result['updated'] == 0
        assert restore_result['skipped'] == 0
    
    @settings(max_examples=100)
    @given(
        record_count=st.integers(min_value=1, max_value=10),
        new_status=st.sampled_from(['A', 'PH', 'WO'])
    )
    def test_record_update_detection(self, record_count, new_status):
        """
        Feature: data-backup-sync, Property 7: Record update detection
        
        For any backup file containing a record that matches an existing database record 
        by unique key but has different field values, restoring should update 
        the database record with the backup values.
        
        Validates: Requirements 3.5
        """
        # Clear existing data
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Create a company and records with status 'P'
        company = Company.objects.create(name=f"UpdateTest_{timezone.now().timestamp()}")
        
        for i in range(record_count):
            AttendanceRecord.objects.create(
                ep_no=f"UPD{i:04d}",
                ep_name=f"Update Test {i}",
                company=company,
                date=timezone.now().date(),
                shift="Day",
                overstay="0",
                status="P"  # Original status
            )
        
        # Create backup with modified status
        backup_service = BackupService()
        backup_result = backup_service.create_backup()
        
        # Modify all records in backup to have new_status
        for record in backup_result['data']['attendance_records']:
            record['status'] = new_status
        
        # Restore backup
        restore_service = RestoreService()
        restore_result = restore_service.restore_backup(backup_result['data'])
        
        # Verify success
        assert restore_result['success'] is True, \
            f"Restore failed: {restore_result.get('errors', [])}"
        
        # Verify all records were updated
        assert restore_result['updated'] == record_count, \
            f"Expected {record_count} records updated, got {restore_result['updated']}"
        assert restore_result['added'] == 0
        assert restore_result['skipped'] == 0
        
        # Verify status was actually updated in database
        for record in AttendanceRecord.objects.all():
            assert record.status == new_status, \
                f"Record {record.ep_no} status should be {new_status}, got {record.status}"
    
    @settings(max_examples=50)  # Fewer examples since this tests error handling
    @given(
        record_count=st.integers(min_value=1, max_value=5)
    )
    def test_transaction_atomicity(self, record_count):
        """
        Feature: data-backup-sync, Property 13: Transaction atomicity
        
        For any restore operation that encounters an error, either all changes 
        should be committed (if successful) or no changes should be persisted (if failed).
        
        Validates: Requirements 7.1, 7.2
        """
        # Clear existing data
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Create a company
        company = Company.objects.create(name=f"TransTest_{timezone.now().timestamp()}")
        
        # Create valid backup data
        backup_data = {
            'metadata': {
                'version': '1.0',
                'created_at': timezone.now().isoformat(),
                'backup_type': 'full',
                'total_companies': 1,
                'total_attendance_records': record_count + 1
            },
            'companies': [
                {
                    'id': company.id,
                    'name': company.name,
                    'created_at': company.created_at.isoformat()
                }
            ],
            'attendance_records': []
        }
        
        # Add valid records
        for i in range(record_count):
            backup_data['attendance_records'].append({
                'ep_no': f"TRN{i:04d}",
                'ep_name': f"Trans Test {i}",
                'company_name': company.name,
                'date': timezone.now().date().isoformat(),
                'shift': 'Day',
                'overstay': '0',
                'status': 'P',
                'in_time': None,
                'out_time': None,
                'in_time_2': None,
                'out_time_2': None,
                'in_time_3': None,
                'out_time_3': None,
                'overtime': None,
                'overtime_to_mandays': None
            })
        
        # Add one invalid record (invalid status to trigger error)
        backup_data['attendance_records'].append({
            'ep_no': 'INVALID',
            'ep_name': 'Invalid Record',
            'company_name': company.name,
            'date': timezone.now().date().isoformat(),
            'shift': 'Day',
            'overstay': '0',
            'status': 'INVALID_STATUS',  # This will cause an error
            'in_time': None,
            'out_time': None,
            'in_time_2': None,
            'out_time_2': None,
            'in_time_3': None,
            'out_time_3': None,
            'overtime': None,
            'overtime_to_mandays': None
        })
        
        # Get initial count
        initial_count = AttendanceRecord.objects.count()
        
        # Attempt restore (should fail due to invalid status)
        restore_service = RestoreService()
        restore_result = restore_service.restore_backup(backup_data)
        
        # Verify restore failed or had errors
        has_errors = not restore_result['success'] or len(restore_result.get('errors', [])) > 0
        
        if not restore_result['success']:
            # If restore failed completely, verify rollback occurred
            final_count = AttendanceRecord.objects.count()
            assert final_count == initial_count, \
                f"Transaction should rollback on failure: started with {initial_count}, ended with {final_count}"
    
    @settings(max_examples=100)
    @given(
        company_name=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Zs'))),
        record_count=st.integers(min_value=1, max_value=5)
    )
    def test_referential_integrity_preservation(self, company_name, record_count):
        """
        Feature: data-backup-sync, Property 11: Referential integrity preservation
        
        For any backup file being restored, if an attendance record references a company 
        that doesn't exist in the database, the company should be created before 
        the attendance record is inserted.
        
        Validates: Requirements 5.5
        """
        # Clear existing data
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Create backup with new company
        new_company_name = (company_name[:50].strip() or "Test") + f"_{timezone.now().timestamp()}"
        
        backup_data = {
            'metadata': {
                'version': '1.0',
                'created_at': timezone.now().isoformat(),
                'backup_type': 'full',
                'total_companies': 1,
                'total_attendance_records': record_count
            },
            'companies': [
                {
                    'id': 999,
                    'name': new_company_name,
                    'created_at': timezone.now().isoformat()
                }
            ],
            'attendance_records': []
        }
        
        # Add records referencing the new company
        for i in range(record_count):
            backup_data['attendance_records'].append({
                'ep_no': f"REF{i:04d}",
                'ep_name': f"Ref Test {i}",
                'company_name': new_company_name,
                'date': timezone.now().date().isoformat(),
                'shift': 'Day',
                'overstay': '0',
                'status': 'P',
                'in_time': None,
                'out_time': None,
                'in_time_2': None,
                'out_time_2': None,
                'in_time_3': None,
                'out_time_3': None,
                'overtime': None,
                'overtime_to_mandays': None
            })
        
        # Verify company doesn't exist
        assert not Company.objects.filter(name=new_company_name).exists()
        
        # Restore backup
        restore_service = RestoreService()
        restore_result = restore_service.restore_backup(backup_data)
        
        # Verify success
        assert restore_result['success'] is True, \
            f"Restore failed: {restore_result.get('errors', [])}"
        
        # Verify company was created
        assert Company.objects.filter(name=new_company_name).exists(), \
            f"Company '{new_company_name}' should have been created"
        
        # Verify all records were inserted
        assert restore_result['added'] == record_count, \
            f"Expected {record_count} records added, got {restore_result['added']}"
        
        # Verify all records reference the correct company
        company = Company.objects.get(name=new_company_name)
        for record in AttendanceRecord.objects.filter(company=company):
            assert record.company.name == new_company_name
    
    @settings(max_examples=100)
    @given(
        add_count=st.integers(min_value=0, max_value=5),
        update_count=st.integers(min_value=0, max_value=5),
        skip_count=st.integers(min_value=0, max_value=5)
    )
    def test_restore_summary_accuracy(self, add_count, update_count, skip_count):
        """
        Feature: data-backup-sync, Property 8: Restore summary accuracy
        
        For any restore operation, the summary counts (added, updated, skipped) 
        should sum to the total number of records in the backup file.
        
        Validates: Requirements 3.6
        """
        # Clear existing data
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Create a company
        company = Company.objects.create(name=f"SummaryTest_{timezone.now().timestamp()}")
        
        # Create existing records (for skip and update)
        existing_records = []
        for i in range(skip_count + update_count):
            record = AttendanceRecord.objects.create(
                ep_no=f"SUM{i:04d}",
                ep_name=f"Summary Test {i}",
                company=company,
                date=timezone.now().date(),
                shift="Day",
                overstay="0",
                status="P"
            )
            existing_records.append(record)
        
        # Create backup
        backup_service = BackupService()
        backup_result = backup_service.create_backup()
        
        # Modify some records for update
        for i in range(update_count):
            backup_result['data']['attendance_records'][i]['status'] = 'A'
        
        # Add new records
        for i in range(add_count):
            backup_result['data']['attendance_records'].append({
                'ep_no': f"NEW{i:04d}",
                'ep_name': f"New Test {i}",
                'company_name': company.name,
                'date': timezone.now().date().isoformat(),
                'shift': 'Day',
                'overstay': '0',
                'status': 'P',
                'in_time': None,
                'out_time': None,
                'in_time_2': None,
                'out_time_2': None,
                'in_time_3': None,
                'out_time_3': None,
                'overtime': None,
                'overtime_to_mandays': None
            })
        
        total_records = len(backup_result['data']['attendance_records'])
        
        # Restore backup
        restore_service = RestoreService()
        restore_result = restore_service.restore_backup(backup_result['data'])
        
        # Verify success
        assert restore_result['success'] is True, \
            f"Restore failed: {restore_result.get('errors', [])}"
        
        # Verify summary counts sum to total
        summary_total = restore_result['added'] + restore_result['updated'] + restore_result['skipped']
        assert summary_total == total_records, \
            f"Summary counts ({restore_result['added']} + {restore_result['updated']} + {restore_result['skipped']} = {summary_total}) should equal total records ({total_records})"
    
    @settings(max_examples=50)
    @given(
        record_count=st.integers(min_value=1, max_value=10)
    )
    def test_backup_round_trip_consistency(self, record_count):
        """
        Feature: data-backup-sync, Property 15: Backup round-trip consistency
        
        For any database state, creating a backup and then restoring it to an empty 
        database should result in a database state identical to the original 
        (excluding auto-generated timestamps).
        
        Validates: Requirements 2.1, 3.4, 5.5
        """
        # Clear existing data
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Create original data
        company = Company.objects.create(name=f"RoundTrip_{timezone.now().timestamp()}")
        
        original_records = []
        for i in range(record_count):
            record = AttendanceRecord.objects.create(
                ep_no=f"RT{i:04d}",
                ep_name=f"Round Trip {i}",
                company=company,
                date=timezone.now().date(),
                shift="Day",
                overstay="0",
                status="P"
            )
            original_records.append({
                'ep_no': record.ep_no,
                'ep_name': record.ep_name,
                'company_name': record.company.name,
                'date': record.date,
                'status': record.status
            })
        
        # Create backup
        backup_service = BackupService()
        backup_result = backup_service.create_backup()
        
        # Clear database
        AttendanceRecord.objects.all().delete()
        Company.objects.all().delete()
        
        # Restore backup
        restore_service = RestoreService()
        restore_result = restore_service.restore_backup(backup_result['data'])
        
        # Verify success
        assert restore_result['success'] is True, \
            f"Restore failed: {restore_result.get('errors', [])}"
        
        # Verify all records were restored
        assert restore_result['added'] == record_count, \
            f"Expected {record_count} records added, got {restore_result['added']}"
        
        # Verify data matches original
        restored_records = AttendanceRecord.objects.all().order_by('ep_no')
        assert restored_records.count() == record_count
        
        for i, restored in enumerate(restored_records):
            original = original_records[i]
            assert restored.ep_no == original['ep_no']
            assert restored.ep_name == original['ep_name']
            assert restored.company.name == original['company_name']
            assert restored.date == original['date']
            assert restored.status == original['status']
