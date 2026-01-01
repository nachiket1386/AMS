# Requirements Document

## Introduction

This document specifies the requirements for an Excel File Upload and Integration feature for the Attendance Management System. The feature enables administrators and authorized users to upload Excel files containing attendance data (punch records, overtime requests, partial day requests, regularization requests, and daily summaries) and makes this data accessible to users based on their roles and permissions. The system must handle multiple file formats, validate data integrity, prevent duplicates, and provide user-specific views of the uploaded data.

## Glossary

- **System**: The Attendance Management System web application
- **User**: Any authenticated person using the system (Employee, Contractor, EIC, Admin)
- **Admin**: System administrator with full access to upload and manage data
- **EIC**: Engineer-in-Charge responsible for approving requests
- **Contractor**: Company representative managing contract employees
- **Employee**: Individual worker whose attendance is tracked
- **EP NO**: Employee Personal Number, unique identifier for each employee
- **Upload Session**: A single file upload operation with validation and import
- **File Type**: Category of Excel file (Punchrecord, ARC Summary, Overtime, Partial Day, Regularization)
- **Validation Error**: Data quality issue detected during file processing
- **Import Log**: Record of upload operations including success/failure details
- **Role-Based View**: Data display filtered according to user's role and permissions
- **Duplicate Record**: Data entry with matching primary key (EP NO + PUNCHDATE) already in database
- **Exception Record**: Attendance data requiring approval (overtime, partial day, regularization)

## Requirements

### Requirement 1

**User Story:** As an administrator, I want to upload Excel files containing attendance data, so that the system can store and process employee attendance records.

#### Acceptance Criteria

1. WHEN an administrator accesses the upload interface THEN the System SHALL display a file upload form with drag-and-drop capability
2. WHEN an administrator selects an Excel file THEN the System SHALL validate the file format is .xls or .xlsx
3. WHEN an administrator uploads a file THEN the System SHALL detect the file type automatically based on column structure
4. WHEN the file type is detected THEN the System SHALL display a preview of the first 10 rows with column mappings
5. WHEN an administrator confirms the upload THEN the System SHALL process all rows and import valid records into the database

### Requirement 2

**User Story:** As an administrator, I want the system to validate uploaded data, so that only correct and complete information is stored in the database.

#### Acceptance Criteria

1. WHEN the System processes an uploaded file THEN the System SHALL validate that EP NO matches the pattern PP\d{10} or VP\d{10}
2. WHEN the System processes an uploaded file THEN the System SHALL validate that PUNCHDATE is a valid date in DD/MM/YYYY format
3. WHEN the System processes an uploaded file THEN the System SHALL validate that CONTRACTOR CODE exists in the contractors table
4. WHEN the System processes time fields THEN the System SHALL validate that time values are in HH:MM or HH:MM:SS format
5. WHEN the System detects validation errors THEN the System SHALL generate an error report listing all invalid rows with specific error messages
6. WHEN validation errors exist THEN the System SHALL allow the administrator to download the error report as CSV
7. WHEN the System detects duplicate records THEN the System SHALL skip duplicates and log them in the import summary

### Requirement 3

**User Story:** As an administrator, I want to see the results of each upload operation, so that I can verify data was imported correctly and address any errors.

#### Acceptance Criteria

1. WHEN an upload operation completes THEN the System SHALL display a summary showing total rows processed, successful imports, skipped duplicates, and validation errors
2. WHEN an upload operation completes THEN the System SHALL store an import log entry with timestamp, filename, user, and operation results
3. WHEN an administrator views the import history THEN the System SHALL display all previous upload operations with their summaries
4. WHEN an administrator selects an import log entry THEN the System SHALL display detailed information including error report if errors occurred
5. WHEN an upload fails completely THEN the System SHALL rollback all changes and display an error message with the failure reason

### Requirement 4

**User Story:** As an employee, I want to view my own attendance records, so that I can track my work hours and request status.

#### Acceptance Criteria

1. WHEN an employee logs into the System THEN the System SHALL display a dashboard showing their attendance summary for the current month
2. WHEN an employee views their attendance THEN the System SHALL display only records where EP NO matches their employee ID
3. WHEN an employee views punch records THEN the System SHALL display date, shift, punch times, hours worked, and status
4. WHEN an employee views requests THEN the System SHALL display their overtime, partial day, and regularization requests with approval status
5. WHEN an employee selects a date range THEN the System SHALL filter displayed records to the selected period

### Requirement 5

**User Story:** As a contractor, I want to view attendance data for all employees under my contractor code, so that I can manage my workforce and submit requests.

#### Acceptance Criteria

1. WHEN a contractor logs into the System THEN the System SHALL display a dashboard showing attendance summary for all employees under their contractor code
2. WHEN a contractor views employee list THEN the System SHALL display only employees where CONTRACTOR CODE matches their contractor code
3. WHEN a contractor selects an employee THEN the System SHALL display that employee's detailed attendance records
4. WHEN a contractor views pending requests THEN the System SHALL display all overtime, partial day, and regularization requests for their employees awaiting approval
5. WHEN a contractor filters by date range THEN the System SHALL apply the filter to all displayed data

### Requirement 6

**User Story:** As a user, I want to search and filter attendance data, so that I can quickly find specific records.

#### Acceptance Criteria

1. WHEN a user enters an EP NO in the search field THEN the System SHALL display all records matching that employee ID within the user's permission scope
2. WHEN a user enters an employee name in the search field THEN the System SHALL display all records for employees with matching names within the user's permission scope
3. WHEN a user selects a date range filter THEN the System SHALL display only records where PUNCHDATE falls within the selected range
4. WHEN a user selects a status filter THEN the System SHALL display only records matching the selected status
5. WHEN a user applies multiple filters THEN the System SHALL display records matching all filter criteria using AND logic

### Requirement 7

**User Story:** As an administrator, I want to manage file upload permissions, so that I can control who can upload different types of attendance data.

#### Acceptance Criteria

1. WHEN an administrator configures upload permissions THEN the System SHALL allow assignment of upload rights by user role and file type
2. WHEN a user without upload permission accesses the upload interface THEN the System SHALL display an access denied message
3. WHEN a user with limited upload permission accesses the upload interface THEN the System SHALL display only file types they are authorized to upload
4. WHEN an administrator views upload audit log THEN the System SHALL display all upload operations with user, timestamp, and file type
5. WHEN an administrator revokes upload permission THEN the System SHALL immediately prevent that user from accessing the upload interface

### Requirement 8

**User Story:** As a system, I want to handle different Excel file formats consistently, so that data from HTML-formatted XLS files and true XLSX files is processed correctly.

#### Acceptance Criteria

1. WHEN the System receives an XLS file THEN the System SHALL attempt to parse it as HTML format first
2. WHEN HTML parsing fails for an XLS file THEN the System SHALL attempt to parse it as binary Excel format
3. WHEN the System receives an XLSX file THEN the System SHALL parse it using the OpenXML format
4. WHEN the System cannot parse a file in any supported format THEN the System SHALL display an error message indicating the file is corrupted or unsupported
5. WHEN the System successfully parses a file THEN the System SHALL normalize all data to consistent formats before validation

### Requirement 9

**User Story:** As a developer, I want the system to maintain data relationships, so that uploaded records are properly linked across different file types.

#### Acceptance Criteria

1. WHEN the System imports employee data THEN the System SHALL create or update employee records in the employees table
2. WHEN the System imports contractor data THEN the System SHALL create or update contractor records in the contractors table
3. WHEN the System imports punch records THEN the System SHALL create foreign key relationships to employees and contractors tables
4. WHEN the System imports exception records THEN the System SHALL create foreign key relationships to employees, contractors, and EIC tables
5. WHEN the System detects a missing foreign key reference THEN the System SHALL create the referenced record if possible or log a validation error

### Requirement 10

**User Story:** As an administrator, I want to export filtered data, so that I can generate reports and share data with stakeholders.

#### Acceptance Criteria

1. WHEN an administrator applies filters to attendance data THEN the System SHALL provide an export button
2. WHEN an administrator clicks the export button THEN the System SHALL generate a CSV file containing all filtered records
3. WHEN the System generates an export file THEN the System SHALL include column headers matching the database field names
4. WHEN the export completes THEN the System SHALL trigger a file download with a filename including the export date and time
5. WHEN an administrator exports data THEN the System SHALL log the export operation with user, timestamp, and record count

### Requirement 11

**User Story:** As a user, I want to see real-time upload progress, so that I know the system is processing my file and can estimate completion time.

#### Acceptance Criteria

1. WHEN a file upload begins THEN the System SHALL display a progress indicator showing percentage complete
2. WHEN the System processes rows THEN the System SHALL update the progress indicator in real-time
3. WHEN the System validates data THEN the System SHALL display the current validation phase
4. WHEN the System imports records THEN the System SHALL display the number of records processed and remaining
5. WHEN the upload completes THEN the System SHALL display a completion message with final statistics
