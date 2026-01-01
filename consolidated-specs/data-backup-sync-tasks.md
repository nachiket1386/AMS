# Implementation Plan

- [x] 1. Create BackupLog model and database migration


  - Create BackupLog model in core/models.py with fields for tracking backup/restore operations
  - Generate and run migration to create the database table
  - Add indexes for performance (user, created_at)
  - _Requirements: Audit logging for all backup/restore operations_




- [ ] 2. Implement BackupService core functionality
  - Create core/services/backup_service.py with BackupService class
  - Implement create_backup() method for full backups
  - Implement _serialize_record() to convert Django models to dictionaries
  - Implement _generate_checksum() using SHA256 for change detection
  - Implement _create_metadata() to add backup metadata


  - _Requirements: 2.1, 2.2, 2.3, 2.4_


- [ ] 2.1 Write property test for backup completeness
  - **Property 2: Backup completeness**
  - **Validates: Requirements 2.1, 2.2**




- [ ] 2.2 Write property test for backup metadata accuracy
  - **Property 3: Backup metadata accuracy**
  - **Validates: Requirements 2.3**

- [x] 2.3 Write property test for checksum consistency


  - **Property 4: Checksum consistency**



  - **Validates: Requirements 2.4**

- [ ] 3. Implement incremental backup functionality
  - Add create_incremental_backup() method to BackupService
  - Filter records by updated_at timestamp
  - Add incremental backup metadata


  - _Requirements: 6.1, 6.2_


- [x] 3.1 Write property test for incremental backup filtering


  - **Property 12: Incremental backup filtering**
  - **Validates: Requirements 6.2**

- [ ] 4. Implement ConflictResolver for merge logic
  - Create core/services/conflict_resolver.py with ConflictResolver class
  - Implement detect_conflicts() to compare records by checksum


  - Implement apply_merge_strategy() with support for 'backup_wins', 'database_wins'
  - Implement _records_differ() to compare records excluding timestamps

  - _Requirements: 5.2, 5.3_




- [ ] 4.1 Write property test for checksum-based change detection
  - **Property 10: Checksum-based change detection**
  - **Validates: Requirements 5.2**

- [ ] 4.2 Write property test for merge strategy application
  - **Property (from 5.3): Merge strategy correctness**
  - **Validates: Requirements 5.3**



- [x] 5. Implement RestoreService core functionality

  - Create core/services/restore_service.py with RestoreService class
  - Implement validate_backup() to check JSON structure and schema
  - Implement _get_unique_key() for record matching (ep_no, company_name, date)

  - Implement preview_changes() to analyze what would be changed without applying
  - _Requirements: 3.1, 3.2, 5.1_


- [ ] 5.1 Write property test for backup validation
  - **Property 14: Backup file validation**


  - **Validates: Requirements 9.1, 9.2**

- [ ] 5.2 Write property test for unique key consistency
  - **Property 9: Unique key consistency**
  - **Validates: Requirements 5.1**



- [x] 6. Implement restore merge logic with transaction safety

  - Implement restore_backup() method in RestoreService
  - Add logic to skip identical records (duplicate prevention)
  - Add logic to insert new records

  - Add logic to update changed records
  - Wrap all operations in database transactions with rollback on error


  - Implement progress callback support
  - _Requirements: 3.3, 3.4, 3.5, 7.1, 7.2_

- [ ] 6.1 Write property test for duplicate prevention
  - **Property 5: Duplicate prevention**
  - **Validates: Requirements 3.3**



- [ ] 6.2 Write property test for new record insertion
  - **Property 6: New record insertion**
  - **Validates: Requirements 3.4**



- [ ] 6.3 Write property test for record update detection
  - **Property 7: Record update detection**
  - **Validates: Requirements 3.5**

- [x] 6.4 Write property test for transaction atomicity

  - **Property 13: Transaction atomicity**
  - **Validates: Requirements 7.1, 7.2**

- [ ] 7. Implement referential integrity and restore summary
  - Add logic to create missing companies before attendance records
  - Generate accurate summary with counts of added, updated, skipped records
  - Log all operations to BackupLog model

  - _Requirements: 3.6, 5.5_


- [ ] 7.1 Write property test for referential integrity preservation
  - **Property 11: Referential integrity preservation**
  - **Validates: Requirements 5.5**

- [ ] 7.2 Write property test for restore summary accuracy
  - **Property 8: Restore summary accuracy**
  - **Validates: Requirements 3.6**


- [ ] 7.3 Write property test for backup round-trip consistency
  - **Property 15: Backup round-trip consistency**
  - **Validates: Requirements 2.1, 3.4, 5.5**



- [ ] 8. Create backup web interface
  - Create core/templates/backup_data.html template
  - Add backup_data_view in core/views.py (root user only)
  - Display options for full and incremental backup
  - Show last backup timestamp from BackupLog
  - Add form to trigger backup creation
  - _Requirements: 8.1, 8.2_


- [ ] 9. Create backup download functionality
  - Add download_backup_view in core/views.py
  - Generate timestamped filename for backup files
  - Return JSON file as downloadable response
  - Store backup metadata in BackupLog
  - _Requirements: 2.5_

- [x] 10. Create restore web interface

  - Create core/templates/restore_data.html template
  - Add restore_data_view in core/views.py (root user only)
  - Add file upload form for backup files
  - Display merge strategy selection (backup_wins, database_wins)
  - _Requirements: 8.3_

- [x] 11. Implement restore preview functionality

  - Add preview_restore_view in core/views.py
  - Call RestoreService.preview_changes() on uploaded file

  - Display counts of records to be added, updated, and skipped
  - Show preview before allowing user to apply changes
  - _Requirements: 8.4, 8.5_

- [ ] 11.1 Write property test for preview accuracy
  - **Property (from 8.5): Preview count accuracy**
  - **Validates: Requirements 8.5**


- [ ] 12. Implement restore apply functionality
  - Add apply_restore_view in core/views.py
  - Call RestoreService.restore_backup() with selected merge strategy

  - Display real-time progress using AJAX/fetch
  - Show detailed summary after completion
  - Handle errors gracefully with rollback

  - _Requirements: 3.6, 7.2_


- [ ] 13. Add URL routes for backup/restore views
  - Add URL patterns in core/urls.py for all backup/restore views
  - Ensure all routes are protected with @role_required(['root'])
  - Add navigation links in base template for root users
  - _Requirements: Web interface access_

- [x] 14. Create backup_data management command

  - Create core/management/commands/backup_data.py
  - Add command-line arguments: --type (full/incremental), --output, --since
  - Implement handle() method to call BackupService
  - Output progress information to console
  - Return appropriate exit codes (0 for success, 1 for failure)
  - Add help text for all options
  - _Requirements: 10.1, 10.3, 10.4, 10.5_


- [ ] 15. Create restore_data management command
  - Create core/management/commands/restore_data.py
  - Add command-line arguments: --input, --strategy, --preview
  - Implement handle() method to call RestoreService
  - Support preview mode that shows changes without applying
  - Output progress and summary to console



  - Return appropriate exit codes
  - Add help text for all options
  - _Requirements: 10.2, 10.3, 10.4, 10.5_

- [ ] 16. Implement root user data visibility
  - Update attendance_list_view to show all data for root users (already implemented)
  - Update dashboard_view to show aggregated statistics for root users (already implemented)
  - Update search functionality to search across all companies for root users (already implemented)
  - Update export functionality to include all companies for root users (already implemented)
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ] 16.1 Write property test for root user data visibility
  - **Property 1: Root user data visibility**
  - **Validates: Requirements 1.1**

- [ ] 17. Add input validation and sanitization
  - Implement JSON schema validation in RestoreService
  - Validate all required fields are present in backup records
  - Sanitize input values to prevent SQL injection
  - Validate data types (dates, times, status values)
  - Reject invalid or corrupted files with detailed error messages
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 17.1 Write property test for input validation
  - **Property (from 9.1, 9.2): Field validation**
  - **Validates: Requirements 9.1, 9.2**

- [ ] 17.2 Write property test for invalid data rejection
  - **Property (from 9.3): Invalid data rejection**
  - **Validates: Requirements 9.3**

- [ ] 17.3 Write property test for input sanitization
  - **Property (from 9.4): Input sanitization**
  - **Validates: Requirements 9.4**

- [ ] 18. Implement batch processing for performance
  - Add batch processing to RestoreService (process 1000 records at a time)
  - Use bulk_create() for inserting new records
  - Use bulk_update() for updating existing records
  - Implement company lookup caching to minimize queries
  - Add progress callback that updates every 1000 records
  - _Requirements: Performance optimization_

- [ ] 19. Add comprehensive error handling
  - Wrap all database operations in try-except blocks
  - Implement proper error messages for all failure scenarios
  - Log all errors with detailed information
  - Ensure transactions rollback on any error
  - Clean up temporary files on error
  - _Requirements: Error handling for all operations_

- [ ] 20. Create backup/restore documentation
  - Add user guide for web interface backup/restore
  - Document management command usage with examples
  - Document backup file format and structure
  - Add troubleshooting guide for common issues
  - Document merge strategies and when to use each
  - _Requirements: User documentation_

- [ ] 21. Final checkpoint - Ensure all tests pass
  - Run all unit tests and property-based tests
  - Verify backup and restore work end-to-end
  - Test with large datasets (10K+ records)
  - Test error scenarios and rollback behavior
  - Verify web interface works correctly
  - Verify management commands work correctly
  - Ask the user if questions arise
