# Implementation Plan

- [ ] 1. Set up database schema and models
- [ ] 1.1 Create Django models for master tables (Employee, Contractor, Plant)
  - Define Employee model with all fields from design
  - Define Contractor model with all fields
  - Define Plant model with all fields
  - Add appropriate indexes and constraints
  - _Requirements: 9.1, 9.2_

- [ ] 1.2 Create Django models for transaction tables (PunchRecord, DailySummary, OvertimeRequest, PartialDayRequest, RegularizationRequest)
  - Define PunchRecord model with unique constraint on (ep_no, punchdate)
  - Define DailySummary model with unique constraint on (ep_no, punchdate)
  - Define OvertimeRequest model with status field
  - Define PartialDayRequest model with manday_conversion field
  - Define RegularizationRequest model with old/new punch times
  - Add foreign key relationships to Employee and Contractor
  - _Requirements: 9.3, 9.4_

- [ ] 1.3 Create Django models for audit tables (ImportLog, ExportLog, UploadPermission)
  - Define ImportLog model with all result fields
  - Define ExportLog model with filters JSONB field
  - Define UploadPermission model with user and file_type
  - _Requirements: 3.2, 10.5, 7.1_

- [ ] 1.4 Create and run database migrations
  - Generate migration files for all models
  - Run migrations to create tables
  - Verify schema matches design document
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [ ]* 1.5 Write property test for employee upsert
  - **Property 26: Employee upsert correctness**
  - **Validates: Requirements 9.1**

- [ ]* 1.6 Write property test for contractor upsert
  - **Property 27: Contractor upsert correctness**
  - **Validates: Requirements 9.2**

- [ ]* 1.7 Write property test for foreign key integrity
  - **Property 28: Foreign key integrity**
  - **Validates: Requirements 9.3, 9.4**

- [ ] 2. Implement file parser service
- [ ] 2.1 Create FileParserService class with parse_file method
  - Implement HTML XLS parsing using pandas.read_html
  - Implement binary XLS parsing using xlrd
  - Implement XLSX parsing using openpyxl
  - Add fallback logic for XLS files (try HTML first, then binary)
  - Return normalized DataFrame
  - _Requirements: 8.1, 8.2, 8.3_

- [ ] 2.2 Implement file type detection based on columns
  - Create detect_file_type method that analyzes DataFrame columns
  - Map column patterns to file types (Punchrecord, ARC Summary, Overtime, Partial Day, Regularization)
  - Return FileType enum value
  - _Requirements: 1.3_

- [ ] 2.3 Implement data normalization
  - Create normalize_data method
  - Standardize column names (convert to lowercase, replace spaces with underscores)
  - Convert dates from DD/MM/YYYY to YYYY-MM-DD
  - Convert times to HH:MM:SS format
  - Handle NaN values appropriately
  - _Requirements: 8.5_

- [ ] 2.4 Add error handling for corrupted files
  - Catch parsing exceptions
  - Return appropriate error messages
  - _Requirements: 8.4_

- [ ]* 2.5 Write property test for file type detection
  - **Property 2: File type detection accuracy**
  - **Validates: Requirements 1.3**

- [ ]* 2.6 Write property test for data normalization
  - **Property 25: Data normalization consistency**
  - **Validates: Requirements 8.5**

- [ ]* 2.7 Write unit tests for file parser
  - Test HTML XLS parsing with sample file
  - Test binary XLS parsing with sample file
  - Test XLSX parsing with sample file
  - Test corrupted file handling
  - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ] 3. Implement data validator service
- [ ] 3.1 Create DataValidatorService class with validation methods
  - Implement validate_ep_no method with regex pattern matching
  - Implement validate_date method with DD/MM/YYYY format check and future date check
  - Implement validate_time method with HH:MM and HH:MM:SS format check
  - Implement validate_foreign_keys method to check contractor codes exist
  - Return ValidationResult objects with is_valid flag and error messages
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ] 3.2 Implement batch validation
  - Create validate_batch method that processes entire DataFrame
  - Collect all validation errors with row numbers
  - Generate ValidationReport with summary statistics
  - _Requirements: 2.5_

- [ ] 3.3 Implement duplicate detection
  - Check for duplicate (ep_no, punchdate) combinations
  - Check against existing database records
  - Return list of duplicate row numbers
  - _Requirements: 2.7_

- [ ]* 3.4 Write property test for EP NO validation
  - **Property 5: EP NO format validation**
  - **Validates: Requirements 2.1**

- [ ]* 3.5 Write property test for date validation
  - **Property 6: Date format validation**
  - **Validates: Requirements 2.2**

- [ ]* 3.6 Write property test for time validation
  - **Property 8: Time format validation**
  - **Validates: Requirements 2.4**

- [ ]* 3.7 Write property test for foreign key validation
  - **Property 7: Foreign key validation**
  - **Validates: Requirements 2.3**

- [ ]* 3.8 Write property test for error report completeness
  - **Property 9: Error report completeness**
  - **Validates: Requirements 2.5**

- [ ]* 3.9 Write property test for duplicate detection
  - **Property 10: Duplicate detection and logging**
  - **Validates: Requirements 2.7**

- [ ] 4. Implement data importer service
- [ ] 4.1 Create DataImporterService class with import methods
  - Implement import_batch method with transaction management
  - Implement create_or_update_employees method using bulk_create/bulk_update
  - Implement create_or_update_contractors method using bulk_create/bulk_update
  - Implement import_punch_records method with duplicate skipping
  - Implement import_exception_records method for overtime/partial day/regularization
  - Use batch size of 1000 for bulk operations
  - _Requirements: 1.5, 9.1, 9.2, 9.3, 9.4_

- [ ] 4.2 Implement transaction rollback on errors
  - Wrap all import operations in database transaction
  - Rollback on any exception
  - Log rollback reason
  - _Requirements: 3.5_

- [ ] 4.3 Implement import logging
  - Create ImportLog entry at start of import
  - Update with results on completion
  - Store error report path if errors occurred
  - _Requirements: 3.2_

- [ ] 4.4 Implement missing foreign key resolution
  - Check if contractor exists before importing employee
  - Create contractor record if data available
  - Log validation error if cannot resolve
  - _Requirements: 9.5_

- [ ]* 4.5 Write property test for transaction rollback
  - **Property 13: Transaction rollback on failure**
  - **Validates: Requirements 3.5**

- [ ]* 4.6 Write property test for import log persistence
  - **Property 12: Import log persistence**
  - **Validates: Requirements 3.2**

- [ ]* 4.7 Write property test for missing foreign key resolution
  - **Property 29: Missing foreign key resolution**
  - **Validates: Requirements 9.5**

- [ ]* 4.8 Write unit tests for data importer
  - Test employee upsert with new records
  - Test employee upsert with existing records
  - Test contractor upsert
  - Test punch record import with duplicates
  - Test exception record import
  - Test transaction rollback on error
  - _Requirements: 1.5, 9.1, 9.2, 9.3, 9.4, 3.5_

- [ ] 5. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement upload API endpoints
- [ ] 6.1 Create upload API view
  - Create POST endpoint /api/upload/
  - Accept multipart/form-data with file
  - Validate file extension (.xls, .xlsx)
  - Validate file size (max 50MB)
  - Check user upload permissions
  - Return upload session ID
  - _Requirements: 1.1, 1.2, 7.2_

- [ ] 6.2 Implement file processing endpoint
  - Create POST endpoint /api/upload/{session_id}/process/
  - Call FileParserService to parse file
  - Call DataValidatorService to validate data
  - Return preview data (first 10 rows) and validation summary
  - _Requirements: 1.4, 2.5_

- [ ] 6.3 Implement import confirmation endpoint
  - Create POST endpoint /api/upload/{session_id}/confirm/
  - Call DataImporterService to import data
  - Return import results with statistics
  - _Requirements: 1.5, 3.1_

- [ ] 6.4 Implement error report download endpoint
  - Create GET endpoint /api/upload/{session_id}/errors/
  - Generate CSV file with validation errors
  - Return file download response
  - _Requirements: 2.6_

- [ ] 6.5 Implement import history endpoint
  - Create GET endpoint /api/imports/
  - Return paginated list of ImportLog entries
  - Filter by user if not admin
  - _Requirements: 3.3_

- [ ] 6.6 Implement import detail endpoint
  - Create GET endpoint /api/imports/{id}/
  - Return detailed ImportLog with error report if available
  - _Requirements: 3.4_

- [ ]* 6.7 Write property test for file extension validation
  - **Property 1: File extension validation**
  - **Validates: Requirements 1.2**

- [ ]* 6.8 Write property test for preview row limit
  - **Property 3: Preview row limit**
  - **Validates: Requirements 1.4**

- [ ]* 6.9 Write property test for complete row processing
  - **Property 4: Complete row processing**
  - **Validates: Requirements 1.5**

- [ ]* 6.10 Write property test for import summary accuracy
  - **Property 11: Import summary accuracy**
  - **Validates: Requirements 3.1**

- [ ] 7. Implement permission service
- [ ] 7.1 Create PermissionService class
  - Implement can_upload method to check user permissions
  - Implement get_query_scope method to return Q object based on role
  - Implement filter_queryset method to apply role-based filtering
  - _Requirements: 7.2, 7.3, 4.2, 5.2_

- [ ] 7.2 Implement permission management endpoints
  - Create POST endpoint /api/permissions/ to grant upload permission
  - Create DELETE endpoint /api/permissions/{id}/ to revoke permission
  - Create GET endpoint /api/permissions/ to list user permissions
  - Restrict to admin users only
  - _Requirements: 7.1, 7.5_

- [ ] 7.3 Implement upload audit log endpoint
  - Create GET endpoint /api/audit/uploads/
  - Return all upload operations with user, timestamp, file type
  - Restrict to admin users only
  - _Requirements: 7.4_

- [ ]* 7.4 Write property test for permission-based file type display
  - **Property 24: Permission-based file type display**
  - **Validates: Requirements 7.3**

- [ ] 8. Implement query API endpoints
- [ ] 8.1 Create attendance query endpoint
  - Create GET endpoint /api/attendance/
  - Accept query parameters: ep_no, employee_name, date_from, date_to, status
  - Apply role-based filtering using PermissionService
  - Return paginated results
  - _Requirements: 4.2, 5.2, 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 8.2 Create punch records endpoint
  - Create GET endpoint /api/punch-records/
  - Apply role-based filtering
  - Return punch records with all required fields
  - _Requirements: 4.3_

- [ ] 8.3 Create requests endpoint
  - Create GET endpoint /api/requests/
  - Return overtime, partial day, and regularization requests
  - Apply role-based filtering
  - Filter by status if provided
  - _Requirements: 4.4, 5.4_

- [ ] 8.4 Create dashboard endpoint
  - Create GET endpoint /api/dashboard/
  - Return attendance summary for current month
  - Apply role-based filtering
  - Include summary statistics and recent records
  - _Requirements: 4.1, 5.1_

- [ ]* 8.5 Write property test for employee data isolation
  - **Property 14: Employee data isolation**
  - **Validates: Requirements 4.2**

- [ ]* 8.6 Write property test for contractor data scope
  - **Property 18: Contractor data scope**
  - **Validates: Requirements 5.2**

- [ ]* 8.7 Write property test for date range filtering
  - **Property 17: Date range filtering accuracy**
  - **Validates: Requirements 4.5, 5.5, 6.3**

- [ ]* 8.8 Write property test for EP NO search with permissions
  - **Property 20: EP NO search with permissions**
  - **Validates: Requirements 6.1**

- [ ]* 8.9 Write property test for name search with permissions
  - **Property 21: Name search with permissions**
  - **Validates: Requirements 6.2**

- [ ]* 8.10 Write property test for status filtering
  - **Property 22: Status filtering accuracy**
  - **Validates: Requirements 6.4**

- [ ]* 8.11 Write property test for multiple filter combination
  - **Property 23: Multiple filter combination**
  - **Validates: Requirements 6.5**

- [ ]* 8.12 Write property test for punch record field completeness
  - **Property 15: Punch record field completeness**
  - **Validates: Requirements 4.3**

- [ ]* 8.13 Write property test for request display completeness
  - **Property 16: Request display completeness**
  - **Validates: Requirements 4.4**

- [ ]* 8.14 Write property test for pending request filtering
  - **Property 19: Pending request filtering**
  - **Validates: Requirements 5.4**

- [ ] 9. Implement export service and endpoints
- [ ] 9.1 Create ExportService class
  - Implement export_to_csv method
  - Implement stream_export method for large datasets
  - Generate filename with date and time
  - _Requirements: 10.2, 10.4_

- [ ] 9.2 Create export endpoint
  - Create POST endpoint /api/export/
  - Accept filters in request body
  - Apply role-based filtering
  - Call ExportService to generate CSV
  - Return file download response
  - _Requirements: 10.1, 10.2_

- [ ] 9.3 Implement export logging
  - Create ExportLog entry for each export
  - Store user, timestamp, record count, and filters
  - _Requirements: 10.5_

- [ ]* 9.4 Write property test for export data accuracy
  - **Property 30: Export data accuracy**
  - **Validates: Requirements 10.2, 10.3**

- [ ]* 9.5 Write property test for export filename format
  - **Property 31: Export filename format**
  - **Validates: Requirements 10.4**

- [ ]* 9.6 Write property test for export operation logging
  - **Property 32: Export operation logging**
  - **Validates: Requirements 10.5**

- [ ] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Implement frontend upload component
- [ ] 11.1 Create FileUpload React component
  - Implement drag-and-drop zone using react-dropzone
  - Add file selection button
  - Validate file extension on client side
  - Display selected file information
  - _Requirements: 1.1, 1.2_

- [ ] 11.2 Implement file upload with progress tracking
  - Use axios to upload file with progress callback
  - Display progress bar showing percentage
  - Update progress in real-time
  - _Requirements: 11.1, 11.2_

- [ ] 11.3 Implement file preview display
  - Fetch preview data from API after upload
  - Display first 10 rows in table format
  - Show column mappings
  - Display validation summary (errors, warnings)
  - _Requirements: 1.4, 11.3_

- [ ] 11.4 Implement import confirmation
  - Add confirm button to proceed with import
  - Show processing status during import
  - Display number of records processed and remaining
  - _Requirements: 1.5, 11.4_

- [ ] 11.5 Implement import results display
  - Show import summary with statistics
  - Display success message with counts
  - Provide download link for error report if errors exist
  - _Requirements: 3.1, 2.6, 11.5_

- [ ] 11.6 Add error handling and user feedback
  - Display error messages for upload failures
  - Show validation errors in preview
  - Handle network errors gracefully
  - _Requirements: 8.4_

- [ ] 12. Implement frontend dashboard component
- [ ] 12.1 Create Dashboard React component
  - Fetch dashboard data from API on mount
  - Display summary cards (total days, present, absent, overtime)
  - Show recent attendance records in table
  - Display pending requests if applicable
  - _Requirements: 4.1, 5.1_

- [ ] 12.2 Add date range selector
  - Implement date range picker component
  - Update dashboard data when range changes
  - Default to current month
  - _Requirements: 4.5, 5.5_

- [ ] 12.3 Add attendance trend chart
  - Use recharts library to display attendance over time
  - Show present/absent/leave breakdown
  - Make chart responsive
  - _Requirements: 4.1, 5.1_

- [ ] 13. Implement frontend search and filter component
- [ ] 13.1 Create SearchFilter React component
  - Add EP NO search input
  - Add employee name search input
  - Add date range picker
  - Add status dropdown filter
  - Add contractor filter (for admin users)
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 13.2 Implement filter application
  - Call API with filter parameters on submit
  - Display filtered results in table
  - Show active filters with remove option
  - Support multiple simultaneous filters
  - _Requirements: 6.5_

- [ ] 13.3 Add export button
  - Show export button when filters are applied
  - Call export API with current filters
  - Trigger file download
  - _Requirements: 10.1, 10.2_

- [ ] 14. Implement frontend permission management (admin only)
- [ ] 14.1 Create PermissionManagement React component
  - Display list of users with their upload permissions
  - Add grant permission form (user selector, file type selector)
  - Add revoke permission button for each permission
  - Restrict access to admin users
  - _Requirements: 7.1, 7.5_

- [ ] 14.2 Create UploadAuditLog React component
  - Display table of all upload operations
  - Show user, timestamp, file type, results
  - Add filtering by user and date range
  - Restrict access to admin users
  - _Requirements: 7.4_

- [ ] 15. Implement frontend import history component
- [ ] 15.1 Create ImportHistory React component
  - Fetch and display list of import operations
  - Show filename, date, user, status, statistics
  - Add pagination for large lists
  - _Requirements: 3.3_

- [ ] 15.2 Implement import detail view
  - Create modal or detail page for import log
  - Display full import details
  - Show error report if available
  - Provide download link for error report
  - _Requirements: 3.4_

- [ ] 16. Add authentication and routing
- [ ] 16.1 Implement authentication flow
  - Add login page
  - Store JWT token in localStorage
  - Add token to API requests
  - Implement token refresh
  - Add logout functionality
  - _Requirements: 4.1, 5.1, 7.2_

- [ ] 16.2 Implement role-based routing
  - Create routes for employee dashboard
  - Create routes for contractor dashboard
  - Create routes for admin dashboard
  - Protect routes based on user role
  - Redirect unauthorized access
  - _Requirements: 4.1, 5.1, 7.2_

- [ ] 17. Add performance optimizations
- [ ] 17.1 Implement database indexing
  - Add index on (ep_no, punchdate)
  - Add index on contractor_code
  - Add index on punchdate
  - Verify query performance
  - _Requirements: Performance_

- [ ] 17.2 Implement query optimization
  - Use select_related for foreign keys
  - Use prefetch_related for reverse relations
  - Use only() to fetch required fields
  - Implement pagination for large result sets
  - _Requirements: Performance_

- [ ] 17.3 Implement caching
  - Cache contractor list with 1-hour TTL
  - Cache user permissions with invalidation on change
  - Cache dashboard summaries with 5-minute TTL
  - Use Redis for cache backend
  - _Requirements: Performance_

- [ ] 17.4 Implement async processing for large uploads
  - Set up Celery with Redis broker
  - Create Celery task for file import
  - Send progress updates via WebSocket
  - Queue exports for background processing
  - _Requirements: 11.2, 11.4_

- [ ] 18. Add security measures
- [ ] 18.1 Implement file upload security
  - Validate file size (max 50MB)
  - Store uploaded files outside web root
  - Use unique filenames (UUID)
  - Add file type validation on server
  - _Requirements: 1.2, Security_

- [ ] 18.2 Implement rate limiting
  - Add rate limiting to upload endpoint (5 uploads per hour per user)
  - Add rate limiting to export endpoint (10 exports per hour per user)
  - Add rate limiting to query endpoints (100 requests per minute per user)
  - _Requirements: Security_

- [ ] 18.3 Add audit logging
  - Log all data access with user and timestamp
  - Log all permission changes
  - Log all failed authentication attempts
  - Store logs in separate audit table
  - _Requirements: 3.2, 7.4, 10.5, Security_

- [ ] 19. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 20. Integration testing and deployment preparation
- [ ] 20.1 Run end-to-end integration tests
  - Test complete upload flow (upload → parse → validate → import)
  - Test role-based access for all user types
  - Test search and filter with various combinations
  - Test export functionality
  - _Requirements: All_

- [ ] 20.2 Perform load testing
  - Test upload with 10K, 50K, 100K row files
  - Test concurrent uploads by multiple users
  - Test query performance with large datasets
  - Verify performance targets are met
  - _Requirements: Performance_

- [ ] 20.3 Perform security testing
  - Test unauthorized access attempts
  - Test SQL injection in search fields
  - Test XSS in file uploads
  - Test session management
  - _Requirements: Security_

- [ ] 20.4 Set up monitoring and logging
  - Configure application metrics collection
  - Set up log aggregation
  - Configure alerting rules
  - Create monitoring dashboard
  - _Requirements: Monitoring_

- [ ] 20.5 Create deployment documentation
  - Document environment setup
  - Document configuration variables
  - Document database migration steps
  - Document backup and recovery procedures
  - _Requirements: Documentation_
