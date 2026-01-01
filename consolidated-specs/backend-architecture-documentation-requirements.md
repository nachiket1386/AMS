# Requirements Document

## Introduction

This document specifies the requirements for comprehensive backend architecture documentation for the Attendance Management System. The system is a Django-based web application that manages employee attendance records with multi-tenant support, role-based access control, CSV import/export capabilities, and audit logging.

## Glossary

- **System**: The Attendance Management System backend
- **User**: An authenticated person using the system with assigned roles
- **Root User**: A user with the highest privilege level who can access all companies and manage all users
- **Admin User**: A company-level administrator who can manage users and data within their assigned company
- **User1**: A basic user with read-only access to their company's data
- **Company**: A tenant organization in the multi-tenant system
- **Attendance Record**: A single entry recording an employee's attendance for a specific date
- **CSV Processor**: The component responsible for parsing and validating CSV files
- **Upload Log**: An audit record of CSV upload operations
- **Role-Based Access Control (RBAC)**: A security mechanism that restricts system access based on user roles
- **Multi-Tenant Architecture**: A software architecture where a single instance serves multiple organizations (tenants)
- **Django ORM**: Django's Object-Relational Mapping system for database operations
- **Decorator**: A Python function that modifies the behavior of another function
- **Middleware**: Software components that process requests and responses in the Django request/response cycle

## Requirements

### Requirement 1: Multi-Tenant Data Architecture

**User Story:** As a system architect, I want a multi-tenant data architecture, so that multiple companies can use the system while maintaining data isolation.

#### Acceptance Criteria

1. THE System SHALL provide a Company model that represents tenant organizations
2. WHEN a Company is created, THE System SHALL assign a unique identifier and timestamp
3. THE System SHALL associate each AttendanceRecord with exactly one Company through a foreign key relationship
4. THE System SHALL associate each User (except Root) with exactly one Company
5. WHEN querying attendance records, THE System SHALL filter results based on the authenticated user's company assignment

### Requirement 2: Role-Based Access Control

**User Story:** As a security administrator, I want role-based access control, so that users have appropriate permissions based on their responsibilities.

#### Acceptance Criteria

1. THE System SHALL support three distinct user roles: Root, Admin, and User1
2. WHEN a Root user accesses data, THE System SHALL grant access to all companies and all records
3. WHEN an Admin user accesses data, THE System SHALL restrict access to their assigned company only
4. WHEN a User1 accesses data, THE System SHALL provide read-only access to their assigned company's data
5. THE System SHALL enforce role validation before executing privileged operations
6. WHEN a user attempts unauthorized access, THE System SHALL return a 403 Forbidden response and log the attempt

### Requirement 3: User Authentication and Management

**User Story:** As an administrator, I want to manage user accounts, so that I can control who has access to the system.

#### Acceptance Criteria

1. THE System SHALL extend Django's AbstractUser model with custom role and company fields
2. WHEN a user logs in, THE System SHALL authenticate credentials against the database
3. WHEN authentication succeeds, THE System SHALL create a session and redirect to the dashboard
4. WHEN authentication fails, THE System SHALL display an error message and log the failed attempt
5. THE System SHALL validate that Admin and User1 roles have an assigned company before saving
6. WHEN a Root user creates a user, THE System SHALL allow assignment of any role and any company
7. WHEN an Admin user creates a user, THE System SHALL restrict creation to User1 role within their company

### Requirement 4: Attendance Record Management

**User Story:** As a user, I want to view and manage attendance records, so that I can track employee attendance data.

#### Acceptance Criteria

1. THE System SHALL store attendance records with employee number, name, company, date, shift, status, and optional time fields
2. THE System SHALL enforce uniqueness constraint on the combination of employee number and date
3. WHEN displaying attendance records, THE System SHALL paginate results with 50 records per page
4. THE System SHALL support filtering by date range, company, employee number, and status
5. WHEN a Root or Admin user edits a record, THE System SHALL validate company access before allowing modification
6. WHEN a record is updated, THE System SHALL automatically update the updated_at timestamp
7. THE System SHALL create database indexes on frequently queried fields for performance optimization

### Requirement 5: CSV Import Processing

**User Story:** As an administrator, I want to import attendance data from CSV files, so that I can bulk upload records efficiently.

#### Acceptance Criteria

1. WHEN a CSV file is uploaded, THE System SHALL validate the file extension is .csv
2. THE System SHALL validate that all required columns are present: EP NO, EP NAME, COMPANY NAME, DATE, SHIFT, STATUS
3. WHEN parsing CSV rows, THE System SHALL validate date format as YYYY-MM-DD or DD-MM-YYYY
4. THE System SHALL reject dates that are in the future
5. THE System SHALL validate time fields in HH:MM format and handle optional (N) suffixes
6. THE System SHALL validate status values against allowed options: P, A, PH, L, -0.5, -1
7. WHEN an Admin user uploads CSV, THE System SHALL restrict company names to their assigned company
8. WHEN a record with matching employee number and date exists, THE System SHALL update the existing record
9. WHEN processing completes, THE System SHALL create an UploadLog with success count, update count, and error details
10. THE System SHALL process CSV files row-by-row and collect all validation errors for reporting

### Requirement 6: Data Export Functionality

**User Story:** As a user, I want to export attendance data, so that I can analyze it in external tools.

#### Acceptance Criteria

1. THE System SHALL support export to both CSV and XLSX formats
2. WHEN exporting data, THE System SHALL apply the same filters as the list view
3. WHEN a Root user exports, THE System SHALL include all companies in the export
4. WHEN an Admin or User1 exports, THE System SHALL include only their company's data
5. WHEN generating XLSX files, THE System SHALL apply header styling with colored background and bold text
6. THE System SHALL auto-adjust column widths in XLSX exports based on content length
7. THE System SHALL include all attendance fields in the export including optional time fields
8. THE System SHALL format dates as DD-MM-YYYY and times as HH:MM in exports

### Requirement 7: Audit Logging and Tracking

**User Story:** As a compliance officer, I want audit logs of all data operations, so that I can track system usage and changes.

#### Acceptance Criteria

1. THE System SHALL create an UploadLog entry for every CSV upload operation
2. WHEN an upload completes, THE System SHALL record the user, timestamp, filename, success count, update count, and error count
3. THE System SHALL store error messages in the UploadLog for failed row processing
4. THE System SHALL log authentication events including successful logins and failed attempts
5. THE System SHALL log permission denial events with user, role, and attempted action
6. WHEN a Root user views logs, THE System SHALL display all upload logs across all companies
7. WHEN an Admin views logs, THE System SHALL display only logs from their company

### Requirement 8: Database Schema and Relationships

**User Story:** As a database administrator, I want a well-designed schema, so that data integrity is maintained and queries are efficient.

#### Acceptance Criteria

1. THE System SHALL define a Company model with name, created_at fields and unique constraint on name
2. THE System SHALL define a User model extending AbstractUser with role, company fields
3. THE System SHALL define an AttendanceRecord model with all attendance fields and foreign key to Company
4. THE System SHALL define an UploadLog model with foreign key to User and audit fields
5. THE System SHALL create database indexes on ep_no+date, company+date, and date fields for AttendanceRecord
6. THE System SHALL create database indexes on user+uploaded_at and uploaded_at fields for UploadLog
7. WHEN a Company is deleted, THE System SHALL cascade delete all associated AttendanceRecords
8. WHEN a Company is deleted, THE System SHALL set User.company to NULL for associated users
9. WHEN a User is deleted, THE System SHALL cascade delete all associated UploadLogs

### Requirement 9: View Layer Architecture

**User Story:** As a developer, I want a well-organized view layer, so that the application is maintainable and follows Django best practices.

#### Acceptance Criteria

1. THE System SHALL implement function-based views for all user-facing endpoints
2. THE System SHALL apply @login_required decorator to all views except login
3. THE System SHALL apply @role_required decorator to views requiring specific roles
4. THE System SHALL apply @company_access_required decorator to views requiring company data access
5. WHEN a view processes a form, THE System SHALL validate data using Django forms
6. WHEN a view encounters an error, THE System SHALL display user-friendly messages using Django messages framework
7. THE System SHALL implement custom error handlers for 403, 404, and 500 status codes
8. THE System SHALL use Django's Paginator for list views with large datasets

### Requirement 10: Security and Validation

**User Story:** As a security engineer, I want comprehensive input validation and security controls, so that the system is protected against common vulnerabilities.

#### Acceptance Criteria

1. THE System SHALL validate all user inputs using Django forms with field-level validation
2. THE System SHALL sanitize CSV input data by stripping whitespace and validating formats
3. THE System SHALL use Django's CSRF protection for all POST requests
4. THE System SHALL hash passwords using Django's password hashing system
5. THE System SHALL validate that dates are not in the future for attendance records
6. THE System SHALL validate employee numbers and names are not empty after stripping whitespace
7. WHEN a validation error occurs, THE System SHALL return descriptive error messages
8. THE System SHALL prevent SQL injection through Django ORM parameterized queries
9. THE System SHALL log security-relevant events including failed authentication and permission denials

### Requirement 11: Configuration and Settings

**User Story:** As a system administrator, I want configurable settings, so that I can deploy the system in different environments.

#### Acceptance Criteria

1. THE System SHALL use Django settings module for all configuration
2. THE System SHALL support SQLite database for development and PostgreSQL for production
3. THE System SHALL configure logging to both console and file outputs
4. THE System SHALL define separate log levels for Django framework and application code
5. THE System SHALL configure static files serving for CSS and JavaScript
6. THE System SHALL define custom user model as AUTH_USER_MODEL setting
7. THE System SHALL configure login, logout, and redirect URLs
8. THE System SHALL use environment-specific DEBUG and ALLOWED_HOSTS settings

### Requirement 12: Error Handling and Resilience

**User Story:** As a user, I want graceful error handling, so that I receive helpful feedback when something goes wrong.

#### Acceptance Criteria

1. WHEN a CSV processing error occurs, THE System SHALL continue processing remaining rows
2. WHEN a database error occurs, THE System SHALL log the error and display a user-friendly message
3. WHEN a file upload fails, THE System SHALL display the specific validation error
4. THE System SHALL catch and handle exceptions in CSV processing without crashing
5. WHEN a 404 error occurs, THE System SHALL render a custom 404 template
6. WHEN a 403 error occurs, THE System SHALL render a custom 403 template
7. WHEN a 500 error occurs, THE System SHALL render a custom 500 template and log the exception
8. THE System SHALL validate file extensions before processing uploaded files
