# Design Document: Data Backup and Synchronization System

## Overview

The Data Backup and Synchronization System provides Git-like functionality for managing attendance data across local development and production environments. The system enables root users to export complete database snapshots, intelligently merge data from backups, and maintain data consistency without creating duplicates.

The design follows a three-layer architecture:
1. **Data Layer**: JSON-based backup format with checksums and metadata
2. **Service Layer**: Backup/restore logic with conflict resolution
3. **Interface Layer**: Web UI and Django management commands

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interfaces                         │
│  ┌──────────────────┐         ┌──────────────────────────┐ │
│  │   Web Interface  │         │  Management Commands     │ │
│  │  - Backup Page   │         │  - backup_data.py        │ │
│  │  - Restore Page  │         │  - restore_data.py       │ │
│  └──────────────────┘         └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Service Layer                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           BackupService                               │  │
│  │  - create_backup()                                    │  │
│  │  - create_incremental_backup()                        │  │
│  │  - validate_backup()                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           RestoreService                              │  │
│  │  - restore_backup()                                   │  │
│  │  - preview_changes()                                  │  │
│  │  - merge_records()                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           ConflictResolver                            │  │
│  │  - detect_conflicts()                                 │  │
│  │  - apply_merge_strategy()                             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌──────────────────┐         ┌──────────────────────────┐ │
│  │  Django Models   │         │   Backup File Format     │ │
│  │  - Company       │         │   (JSON)                 │ │
│  │  - Attendance    │         │   - Metadata             │ │
│  │  - User          │         │   - Companies            │ │
│  └──────────────────┘         │   - Attendance Records   │ │
│                                │   - Checksums            │ │
│                                └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

**Backup Flow:**
```
User Request → BackupService → Query Database → Generate Checksums 
→ Create JSON → Add Metadata → Return File
```

**Restore Flow:**
```
Upload File → Validate Format → Preview Changes → User Confirms 
→ RestoreService → Merge Records → Update Database → Return Summary
```

## Components and Interfaces

### 1. BackupService

**Responsibility**: Create backup files from database

**Methods**:

```python
class BackupService:
    def create_backup(self, backup_type='full', since_date=None) -> dict:
        """
        Create a backup of attendance data
        
        Args:
            backup_type: 'full' or 'incremental'
            since_date: For incremental backups, only include records modified after this date
            
        Returns:
            dict with keys: 'success', 'file_path', 'record_count', 'metadata'
        """
        
    def _generate_checksum(self, record) -> str:
        """Generate SHA256 checksum for a record"""
        
    def _serialize_record(self, record) -> dict:
        """Convert Django model instance to dict"""
        
    def _create_metadata(self, record_count) -> dict:
        """Create backup metadata"""
```

**Backup File Format**:

```json
{
  "metadata": {
    "version": "1.0",
    "created_at": "2025-11-25T10:30:00Z",
    "backup_type": "full",
    "total_companies": 5,
    "total_attendance_records": 1500,
    "created_by": "root_user"
  },
  "companies": [
    {
      "id": 1,
      "name": "ABC Corp",
      "created_at": "2025-01-15T08:00:00Z",
      "checksum": "a1b2c3d4..."
    }
  ],
  "attendance_records": [
    {
      "ep_no": "EMP001",
      "ep_name": "John Doe",
      "company_name": "ABC Corp",
      "date": "2025-11-20",
      "shift": "Day",
      "status": "P",
      "in_time": "09:00",
      "out_time": "17:00",
      "overstay": "0",
      "checksum": "e5f6g7h8..."
    }
  ]
}
```

### 2. RestoreService

**Responsibility**: Restore data from backup files with intelligent merging

**Methods**:

```python
class RestoreService:
    def __init__(self, conflict_resolver):
        self.conflict_resolver = conflict_resolver
        
    def validate_backup(self, file_path) -> dict:
        """
        Validate backup file structure and content
        
        Returns:
            dict with keys: 'valid', 'errors', 'warnings'
        """
        
    def preview_changes(self, file_path) -> dict:
        """
        Analyze what changes would be made without applying them
        
        Returns:
            dict with keys: 'to_add', 'to_update', 'to_skip', 'conflicts'
        """
        
    def restore_backup(self, file_path, merge_strategy='backup_wins', 
                      progress_callback=None) -> dict:
        """
        Restore data from backup file
        
        Args:
            file_path: Path to backup JSON file
            merge_strategy: 'backup_wins', 'database_wins', or 'manual'
            progress_callback: Function to call with progress updates
            
        Returns:
            dict with keys: 'success', 'added', 'updated', 'skipped', 'errors'
        """
        
    def _get_unique_key(self, record) -> tuple:
        """Generate unique key for record matching"""
        return (record['ep_no'], record['company_name'], record['date'])
```

### 3. ConflictResolver

**Responsibility**: Handle data conflicts during restore

**Methods**:

```python
class ConflictResolver:
    def detect_conflicts(self, backup_record, db_record) -> bool:
        """Check if two records conflict (same key, different data)"""
        
    def apply_merge_strategy(self, backup_record, db_record, strategy) -> dict:
        """
        Apply merge strategy to resolve conflict
        
        Args:
            backup_record: Record from backup file
            db_record: Existing database record
            strategy: 'backup_wins', 'database_wins', or 'manual'
            
        Returns:
            dict representing the merged record
        """
        
    def _records_differ(self, record1, record2) -> bool:
        """Compare two records excluding timestamps and checksums"""
```

### 4. Web Views

**Backup View** (`backup_data_view`):
- Display backup options (full/incremental)
- Show last backup timestamp
- Trigger backup creation
- Provide download link

**Restore View** (`restore_data_view`):
- File upload form
- Preview changes before applying
- Merge strategy selection
- Progress display
- Results summary

**URL Routes**:
```python
path('backup/', backup_data_view, name='backup_data'),
path('backup/download/<str:filename>/', download_backup_view, name='download_backup'),
path('restore/', restore_data_view, name='restore_data'),
path('restore/preview/', preview_restore_view, name='preview_restore'),
path('restore/apply/', apply_restore_view, name='apply_restore'),
```

### 5. Management Commands

**backup_data.py**:
```bash
python manage.py backup_data --type full --output /path/to/backup.json
python manage.py backup_data --type incremental --since 2025-11-01
```

**restore_data.py**:
```bash
python manage.py restore_data --input /path/to/backup.json --strategy backup_wins
python manage.py restore_data --input backup.json --preview  # Preview only
```

## Data Models

### Existing Models (No Changes Required)

The system uses existing models:
- `Company`: Already has all required fields
- `AttendanceRecord`: Already has all required fields including `created_at` and `updated_at` for incremental backups
- `User`: Already has role-based access control

### New Model: BackupLog

Track backup and restore operations:

```python
class BackupLog(models.Model):
    """Audit log for backup and restore operations"""
    OPERATION_CHOICES = [
        ('backup_full', 'Full Backup'),
        ('backup_incremental', 'Incremental Backup'),
        ('restore', 'Restore'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES)
    filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Statistics
    companies_count = models.IntegerField(default=0)
    records_count = models.IntegerField(default=0)
    records_added = models.IntegerField(default=0)  # For restore
    records_updated = models.IntegerField(default=0)  # For restore
    records_skipped = models.IntegerField(default=0)  # For restore
    
    # Status
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Root user data visibility
*For any* attendance record in the database, when a root user queries the attendance list, that record should be included in the results regardless of which company it belongs to.
**Validates: Requirements 1.1**

### Property 2: Backup completeness
*For any* database state, when a full backup is created, the backup file should contain exactly the same number of companies and attendance records as exist in the database at that moment.
**Validates: Requirements 2.1, 2.2**

### Property 3: Backup metadata accuracy
*For any* backup file created, the metadata section should accurately reflect the counts of companies and attendance records contained in the backup data section.
**Validates: Requirements 2.3**

### Property 4: Checksum consistency
*For any* record in a backup file, if the record data has not changed, generating a new checksum for that record should produce the same checksum value.
**Validates: Requirements 2.4**

### Property 5: Duplicate prevention
*For any* backup file and database state, when restoring records that already exist in the database with identical data, those records should be skipped and not create duplicates.
**Validates: Requirements 3.3**

### Property 6: New record insertion
*For any* backup file containing a record with a unique key (ep_no, company, date) that does not exist in the database, restoring that backup should insert the new record into the database.
**Validates: Requirements 3.4**

### Property 7: Record update detection
*For any* backup file containing a record that matches an existing database record by unique key but has different field values, restoring should update the database record with the backup values.
**Validates: Requirements 3.5**

### Property 8: Restore summary accuracy
*For any* restore operation, the summary counts (added, updated, skipped) should sum to the total number of records in the backup file.
**Validates: Requirements 3.6**

### Property 9: Unique key consistency
*For any* two attendance records, if they have the same ep_no, company_name, and date, they should be considered the same record for merge purposes.
**Validates: Requirements 5.1**

### Property 10: Checksum-based change detection
*For any* two records with the same unique key, if their checksums differ, the records should be detected as having different data.
**Validates: Requirements 5.2**

### Property 11: Referential integrity preservation
*For any* backup file being restored, if an attendance record references a company that doesn't exist in the database, the company should be created before the attendance record is inserted.
**Validates: Requirements 5.5**

### Property 12: Incremental backup filtering
*For any* incremental backup created with a since_date parameter, all records in the backup should have an updated_at timestamp greater than or equal to since_date.
**Validates: Requirements 6.2**

### Property 13: Transaction atomicity
*For any* restore operation that encounters an error, either all changes should be committed (if successful) or no changes should be persisted (if failed).
**Validates: Requirements 7.1, 7.2, 7.3**

### Property 14: Backup file validation
*For any* uploaded file, if it does not conform to the expected JSON schema with required fields (metadata, companies, attendance_records), the validation should reject the file.
**Validates: Requirements 9.1, 9.2**

### Property 15: Backup round-trip consistency
*For any* database state, creating a backup and then restoring it to an empty database should result in a database state identical to the original (excluding auto-generated timestamps).
**Validates: Requirements 2.1, 3.4, 5.5**

## Error Handling

### Validation Errors

**Invalid File Format**:
- Check JSON structure
- Verify required fields exist
- Validate data types
- Return detailed error messages

**Missing References**:
- Check company references before inserting attendance records
- Create missing companies automatically
- Log warnings for auto-created entities

**Data Integrity Errors**:
- Validate date formats
- Check status values against allowed choices
- Ensure required fields are present
- Sanitize input to prevent injection

### Runtime Errors

**Database Errors**:
- Wrap all database operations in try-except blocks
- Use transactions for restore operations
- Rollback on any error
- Log detailed error information

**File System Errors**:
- Handle missing files gracefully
- Check disk space before creating backups
- Use temporary files for uploads
- Clean up temporary files on error

**Memory Errors**:
- Process large backups in batches
- Use iterators instead of loading entire file
- Implement progress callbacks to prevent timeouts
- Set reasonable file size limits

### User-Facing Error Messages

```python
ERROR_MESSAGES = {
    'invalid_json': 'The uploaded file is not valid JSON',
    'missing_metadata': 'Backup file is missing required metadata',
    'invalid_schema': 'Backup file structure does not match expected format',
    'company_mismatch': 'Some records reference non-existent companies',
    'database_error': 'Database error occurred during restore',
    'permission_denied': 'Only root users can perform backup/restore operations',
}
```

## Testing Strategy

### Unit Testing

**Test Coverage**:
- BackupService methods (create_backup, generate_checksum, serialize_record)
- RestoreService methods (validate_backup, preview_changes, restore_backup)
- ConflictResolver methods (detect_conflicts, apply_merge_strategy)
- Utility functions (unique key generation, checksum calculation)

**Test Data**:
- Create fixtures with known companies and attendance records
- Use factories for generating test data
- Test edge cases (empty database, single record, large datasets)

**Example Unit Tests**:
```python
def test_backup_creates_valid_json():
    """Test that backup creates properly formatted JSON"""
    
def test_restore_skips_duplicates():
    """Test that identical records are not duplicated"""
    
def test_checksum_detects_changes():
    """Test that checksum changes when data changes"""
```

### Property-Based Testing

The system will use **Hypothesis** for Python property-based testing. Each property test will run a minimum of 100 iterations with randomly generated data.

**Property Test Configuration**:
```python
from hypothesis import given, settings
from hypothesis import strategies as st

@settings(max_examples=100)
@given(...)
def test_property_name(...):
    pass
```

**Test Strategies**:
- Generate random companies with valid names
- Generate random attendance records with valid field values
- Generate random dates within reasonable ranges
- Generate random status values from allowed choices

**Property Tests** (one test per correctness property):

1. **test_root_user_sees_all_data**: Generate random companies and records, verify root user query returns all
2. **test_backup_completeness**: Create random data, backup, verify counts match
3. **test_backup_metadata_accuracy**: Generate backup, verify metadata matches data section
4. **test_checksum_consistency**: Generate record, compute checksum twice, verify equality
5. **test_duplicate_prevention**: Create record, backup, restore, verify no duplicates
6. **test_new_record_insertion**: Generate new record in backup, restore, verify insertion
7. **test_record_update_detection**: Modify record in backup, restore, verify update
8. **test_restore_summary_accuracy**: Restore backup, verify sum of counts equals total
9. **test_unique_key_consistency**: Generate records with same key, verify treated as same
10. **test_checksum_change_detection**: Modify record, verify checksum differs
11. **test_referential_integrity**: Backup with new company, restore, verify company created
12. **test_incremental_backup_filtering**: Generate records with timestamps, verify filtering
13. **test_transaction_atomicity**: Simulate error during restore, verify rollback
14. **test_backup_validation**: Generate invalid JSON, verify rejection
15. **test_backup_round_trip**: Backup and restore, verify database state unchanged

### Integration Testing

**End-to-End Scenarios**:
1. Full backup → Restore to empty database → Verify data integrity
2. Incremental backup → Restore → Verify only new records added
3. Backup from production → Restore to local → Verify merge behavior
4. Multiple backups → Restore latest → Verify correct version restored

**Web Interface Testing**:
- Test backup page renders correctly for root user
- Test restore page file upload and preview
- Test progress indicators update correctly
- Test error messages display properly

**Management Command Testing**:
- Test command-line arguments parsing
- Test output formatting
- Test exit codes
- Test file path handling

### Performance Testing

**Benchmarks**:
- Backup creation time for 10K, 100K, 1M records
- Restore time for various dataset sizes
- Memory usage during large operations
- Database query optimization

**Optimization Targets**:
- Backup creation: < 1 second per 1000 records
- Restore with merge: < 2 seconds per 1000 records
- Memory usage: < 500MB for 100K records
- Progress updates: Every 1000 records or 1 second

## Security Considerations

### Access Control

- Only root users can create backups
- Only root users can restore backups
- Validate user role before any backup/restore operation
- Log all backup/restore operations with user information

### Data Validation

- Sanitize all input from backup files
- Validate data types and formats
- Check for SQL injection attempts
- Limit file upload sizes (max 100MB)

### File Handling

- Store backups in secure directory outside web root
- Use secure file names (no path traversal)
- Clean up temporary files immediately
- Encrypt backup files (future enhancement)

## Performance Optimization

### Batch Processing

```python
BATCH_SIZE = 1000  # Process records in batches

def restore_in_batches(records):
    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i:i+BATCH_SIZE]
        with transaction.atomic():
            process_batch(batch)
```

### Database Optimization

- Use `bulk_create()` for inserting multiple records
- Use `bulk_update()` for updating multiple records
- Use `select_related()` to minimize queries
- Drop and rebuild indexes during large restores (like CSV upload)

### Caching

- Cache company lookups during restore
- Use dictionary for fast unique key lookups
- Cache checksums to avoid recalculation

## Future Enhancements

1. **Encryption**: Encrypt backup files with password
2. **Compression**: Compress backup files to reduce size
3. **Cloud Storage**: Upload backups to S3/Azure/GCS
4. **Scheduled Backups**: Automatic daily/weekly backups
5. **Differential Backups**: Only store changed fields
6. **Backup Versioning**: Keep multiple backup versions
7. **Conflict Resolution UI**: Manual conflict resolution interface
8. **Backup Comparison**: Compare two backup files
9. **Selective Restore**: Restore only specific companies or date ranges
10. **Audit Trail**: Detailed change tracking for compliance
