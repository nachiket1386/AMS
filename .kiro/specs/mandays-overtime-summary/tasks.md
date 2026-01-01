# Implementation Plan: Mandays and Overtime Summary

- [x] 1. Create database models and migrations


  - Create MandaySummaryRecord model with all required and optional fields
  - Create MandayUploadLog model for audit logging
  - Add unique constraint on (ep_no, punch_date)
  - Add database indexes for performance
  - Generate and apply Django migrations
  - _Requirements: 2.1, 3.1, 3.3, 5.3, 5.4, 5.5_



- [x] 1.1 Write property test for model validation



  - **Property 10: Numeric field validation**
  - **Validates: Requirements 5.3, 5.4, 5.5, 5.6**

- [ ] 2. Implement MandayProcessor class
  - Create core/manday_processor.py file
  - Implement file reading methods (CSV, XLS, XLSX support)
  - Implement column validation for mandatory fields
  - Implement row-level validation for mandatory fields
  - Implement date validation (format and future date check)
  - Implement decimal validation for numeric fields
  - Implement column extraction logic

  - Implement bulk record creation with upsert logic
  - Add progress tracking callback support
  - _Requirements: 1.2, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 5.2, 5.3, 5.4, 5.5, 5.6_


- [ ] 2.1 Write property test for file format validation
  - **Property 1: File format validation**

  - **Validates: Requirements 1.2, 1.4**

- [x] 2.2 Write property test for mandatory column presence

  - **Property 2: Mandatory column presence**
  - **Validates: Requirements 2.1, 2.2**


- [ ] 2.3 Write property test for mandatory field validation
  - **Property 3: Mandatory field validation**
  - **Validates: Requirements 2.3, 2.4, 2.5**


- [ ] 2.4 Write property test for column extraction
  - **Property 4: Column extraction**

  - **Validates: Requirements 3.1, 3.2**



- [ ] 2.5 Write property test for optional field handling
  - **Property 5: Optional field handling**
  - **Validates: Requirements 3.3**

- [ ] 2.6 Write property test for numeric data type preservation
  - **Property 6: Numeric data type preservation**
  - **Validates: Requirements 3.4**

- [x] 2.7 Write property test for date format validation

  - **Property 9: Date format validation**
  - **Validates: Requirements 5.2**


- [ ] 3. Implement upload view and functionality
  - Create upload_mandays_view function with @role_required decorator
  - Implement file upload handling (POST request)

  - Implement file validation (format, size)
  - Integrate MandayProcessor for file processing

  - Implement progress tracking
  - Create MandayUploadLog entries
  - Display success/error messages to user
  - Handle company association for admin users
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 4.1, 4.2, 4.3, 4.4, 4.5, 7.2_

- [ ] 3.1 Write property test for upload results reporting
  - **Property 7: Upload results reporting**

  - **Validates: Requirements 4.1, 4.2, 4.3**

- [ ] 3.2 Write property test for error detail reporting
  - **Property 8: Error detail reporting**
  - **Validates: Requirements 4.4**

- [ ] 3.3 Write property test for company data isolation
  - **Property 13: Company data isolation**

  - **Validates: Requirements 7.2**

- [ ] 4. Implement list/view functionality
  - Create mandays_list_view function with access control
  - Implement queryset filtering by user role (root vs admin vs user1)


  - Implement date range filtering
  - Implement employee number filtering
  - Implement pagination (50 records per page)
  - Add company access control checks
  - _Requirements: 6.1, 6.2, 6.3, 6.4_



- [ ] 5. Implement export functionality
  - Create mandays_export_view function
  - Implement XLSX export with openpyxl
  - Apply same filters as list view
  - Format headers with styling
  - Auto-adjust column widths
  - Generate timestamped filename


  - _Requirements: 6.5_

- [ ] 6. Implement template download
  - Create download_mandays_template view
  - Generate CSV with correct column headers
  - Include all required and optional columns
  - _Requirements: 1.1_



- [ ] 7. Create URL patterns
  - Add URL pattern for upload view
  - Add URL pattern for list view
  - Add URL pattern for export view

  - Add URL pattern for template download
  - Update core/urls.py with new patterns
  - _Requirements: All_

- [ ] 8. Create upload template
  - Create core/templates/upload_mandays.html
  - Add file upload form with file input

  - Add recent upload logs display
  - Add link to download template
  - Style consistently with existing upload page

  - Add progress indicator for large uploads
  - _Requirements: 1.1, 4.1, 4.2, 4.3, 4.4, 4.5_


- [ ] 9. Create list template
  - Create core/templates/mandays_list.html
  - Add table with all manday fields
  - Add date range filter inputs
  - Add employee number filter input
  - Add pagination controls
  - Add export button

  - Style consistently with attendance_list.html
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 10. Add navigation menu items

  - Add "Upload Mandays" link to navigation (USER2/USER3 only)
  - Add "View Mandays" link to navigation (all authenticated users)

  - Update core/templates/base.html navigation
  - _Requirements: 7.1, 7.2, 7.3_

- [ ] 11. Implement access control
  - Add role checks to upload view (USER2/USER3 only)
  - Add role checks to list view (with company filtering)


  - Add authentication checks (redirect to login)
  - Test access denial for USER1 role
  - _Requirements: 7.1, 7.2, 7.3_

- [ ] 11.1 Write property test for access control enforcement
  - **Property 11: Access control enforcement**
  - **Validates: Requirements 7.1**

- [ ] 11.2 Write property test for admin access grant
  - **Property 12: Admin access grant**
  - **Validates: Requirements 7.2**

- [ ] 12. Add logging and error handling
  - Add logging for upload operations
  - Add logging for validation errors
  - Add logging for access control violations
  - Implement user-friendly error messages
  - Implement error message truncation (show first 5 errors)
  - _Requirements: 4.3, 4.4_

- [ ] 12.1 Write unit tests for error handling
  - Test file upload errors (invalid format, missing file, size limit)
  - Test validation errors (missing columns, invalid data types)
  - Test processing errors (database errors, permission errors)
  - _Requirements: 1.3, 1.4, 2.2, 5.6_

- [ ] 13. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. Write integration tests
  - Test complete upload workflow (file upload → processing → storage)
  - Test list view with filtering and pagination
  - Test export functionality with filtered data
  - Test template download functionality
  - _Requirements: All_

- [ ] 15. Final Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
