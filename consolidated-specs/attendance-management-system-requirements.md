# Requirements Document

## Introduction

The Attendance Management System is a multi-user company data management application that enables organizations to upload, manage, and export employee attendance records via CSV files. The system implements role-based access control with three distinct user roles (Root, Admin, User1) and provides comprehensive data validation, audit logging, and export capabilities.

## Glossary

- **System**: The Attendance Management System application
- **Root User**: A user with unrestricted access to all companies and system functions
- **Admin User**: A user with full access limited to their assigned company
- **User1**: A user with read-only access limited to their assigned company
- **CSV File**: Comma-Separated Values file containing attendance records
- **Attendance Record**: A single employee attendance entry for a specific date
- **Upload Log**: An audit record tracking CSV upload operations
- **Employee Number (EP NO)**: Unique identifier for an employee
- **Status Value**: Attendance status indicator (P=Present, A=Absent, PH=Public Holiday, -0.5=Half day, -1=Full day leave)
- **Duplicate Record**: An attendance record with matching Employee Number and Date

## Requirements

### Requirement 1: User Authentication and Authorization

**User Story:** As a system administrator, I want role-based access control so that users can only access data and functions appropriate to their role.

#### Acceptance Criteria

1. WHEN a user attempts to log in, THE System SHALL authenticate the user credentials against stored user records
2. WHEN authentication succeeds, THE System SHALL create a session for the authenticated user
3. THE System SHALL assign exactly one role (Root, Admin, or User1) to each user account
4. WHERE a user has Admin or User1 role, THE System SHALL associate the user with exactly one company
5. WHEN a user attempts to access a protected resource, THE System SHALL verify the user has appropriate role permissions before granting access

### Requirement 2: CSV File Upload and Validation

**User Story:** As an Admin user, I want to upload CSV files containing attendance data so that I can efficiently import bulk attendance records for my company.

#### Acceptance Criteria

1. WHEN a Root user uploads a CSV file, THE System SHALL accept attendance records for any company specified in the file
2. WHEN an Admin user uploads a CSV file, THE System SHALL accept only attendance records matching the Admin's assigned company
3. WHEN a User1 attempts to upload a CSV file, THE System SHALL reject the upload request with an authorization error
4. WHEN the System processes a CSV file, THE System SHALL validate that all mandatory fields (EP NO, EP NAME, COMPANY NAME, DATE, SHIFT, OVERSTAY, STATUS) are present in each record
5. WHEN the System encounters a DATE field, THE System SHALL validate the date follows YYYY-MM-DD format
6. WHEN the System encounters a DATE field with a future date, THE System SHALL reject the record with a validation error
7. WHEN the System encounters time fields (IN, OUT, IN (2), OUT (2), IN (3), OUT (3), OVERTIME, OVERTIME TO MANDAYS), THE System SHALL validate each time follows HH:MM format
8. WHEN the System encounters a STATUS field, THE System SHALL validate the value is one of: P, A, PH, -0.5, -1
9. WHEN the System encounters a duplicate record (matching EP NO and DATE), THE System SHALL update the existing record with new values
10. WHEN CSV validation completes, THE System SHALL create an Upload Log entry recording success count, update count, and error count

### Requirement 3: Attendance Data Management

**User Story:** As an Admin user, I want to view, edit, and delete attendance records for my company so that I can maintain accurate attendance data.

#### Acceptance Criteria

1. WHEN a Root user requests attendance data, THE System SHALL display records from all companies
2. WHEN an Admin user requests attendance data, THE System SHALL display only records matching the Admin's assigned company
3. WHEN a User1 requests attendance data, THE System SHALL display only records matching the User1's assigned company
4. WHEN a Root user modifies an attendance record, THE System SHALL save the changes for any company
5. WHEN an Admin user modifies an attendance record, THE System SHALL save the changes only if the record belongs to the Admin's assigned company
6. WHEN a User1 attempts to modify an attendance record, THE System SHALL reject the modification request with an authorization error
7. WHEN a Root user deletes an attendance record, THE System SHALL remove the record for any company
8. WHEN an Admin user deletes an attendance record, THE System SHALL remove the record only if it belongs to the Admin's assigned company
9. WHEN a User1 attempts to delete an attendance record, THE System SHALL reject the deletion request with an authorization error

### Requirement 4: Data Export

**User Story:** As a user, I want to export attendance data as CSV files so that I can analyze data in external tools or create backups.

#### Acceptance Criteria

1. WHEN a Root user requests data export, THE System SHALL generate a CSV file containing all attendance records matching applied filters
2. WHEN an Admin user requests data export, THE System SHALL generate a CSV file containing only records from the Admin's assigned company matching applied filters
3. WHEN a User1 requests data export, THE System SHALL generate a CSV file containing only records from the User1's assigned company matching applied filters
4. WHEN the System generates an export CSV file, THE System SHALL include all attendance record fields in the output
5. WHEN the System generates an export CSV file, THE System SHALL format the file to be compatible with the upload CSV format

### Requirement 5: User Management

**User Story:** As a Root user, I want to create and manage user accounts so that I can control system access for my organization.

#### Acceptance Criteria

1. WHEN a Root user creates a new user account, THE System SHALL allow assignment of any role (Root, Admin, or User1)
2. WHEN a Root user creates a new Admin or User1 account, THE System SHALL require assignment of a company
3. WHEN an Admin user creates a new user account, THE System SHALL allow creation of User1 accounts only
4. WHEN an Admin user creates a new User1 account, THE System SHALL automatically assign the Admin's company to the new user
5. WHEN a User1 attempts to create a user account, THE System SHALL reject the request with an authorization error
6. WHEN a Root user modifies an existing user account, THE System SHALL allow changes to any user attribute including role and company
7. WHEN an Admin user modifies an existing User1 account, THE System SHALL allow changes only to User1 accounts in the Admin's company

### Requirement 6: Upload Audit Logging

**User Story:** As a Root user, I want to view logs of all CSV upload operations so that I can track data changes and troubleshoot upload issues.

#### Acceptance Criteria

1. WHEN a CSV upload operation completes, THE System SHALL create an Upload Log entry
2. WHEN the System creates an Upload Log entry, THE System SHALL record the uploading user identifier
3. WHEN the System creates an Upload Log entry, THE System SHALL record the upload timestamp
4. WHEN the System creates an Upload Log entry, THE System SHALL record the count of successfully created records
5. WHEN the System creates an Upload Log entry, THE System SHALL record the count of updated records
6. WHEN the System creates an Upload Log entry, THE System SHALL record the count of records with validation errors
7. WHEN the System creates an Upload Log entry with validation errors, THE System SHALL store error messages for debugging purposes
8. WHEN a Root user requests upload logs, THE System SHALL display all upload logs from all users
9. WHEN an Admin user requests upload logs, THE System SHALL display only upload logs from users in the Admin's company

### Requirement 7: System Administration

**User Story:** As a Root user, I want access to Django admin interface so that I can perform advanced system configuration and data management.

#### Acceptance Criteria

1. THE System SHALL provide a Django admin interface accessible at /admin URL path
2. WHEN a Root user accesses the admin interface, THE System SHALL grant full access to all models and configurations
3. WHEN a non-Root user attempts to access the admin interface, THE System SHALL reject the request with an authorization error
4. WHEN the System starts, THE System SHALL use SQLite as the database backend
5. THE System SHALL store all data in a single SQLite database file named db.sqlite3
