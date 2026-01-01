# Requirements Document

## Introduction

This feature adds a new data upload and summary capability to the attendance management system for tracking final mandays and overtime. The system shall allow administrators to upload Excel files containing employee manday and overtime data, validate the required fields, and store the information for reporting and analysis purposes.

## Glossary

- **Mandays Summary System**: The subsystem responsible for processing and storing employee manday and overtime data
- **epNo**: Employee Number - unique identifier for each employee
- **punchDate**: The date for which mandays and overtime are recorded
- **trade**: The trade or job category of the employee
- **skill**: The skill level or classification of the employee
- **contract**: The contract identifier under which the employee is working
- **plant**: The plant or location code where work was performed
- **mandays**: The number of mandays worked by the employee
- **regularMandayHr**: Regular manday hours worked
- **ot**: Overtime hours worked
- **plantDesc**: Plant description or name
- **Administrator**: A user with USER2 or USER3 role who can upload and manage manday data

## Requirements

### Requirement 1

**User Story:** As an administrator, I want to upload Excel files containing manday and overtime data, so that I can import employee work records into the system.

#### Acceptance Criteria

1. WHEN an administrator accesses the mandays upload page THEN the Mandays Summary System SHALL display a file upload interface accepting CSV, XLS, and XLSX file formats
2. WHEN an administrator selects a valid Excel file THEN the Mandays Summary System SHALL accept the file for processing
3. WHEN an administrator uploads a file larger than 10MB THEN the Mandays Summary System SHALL reject the file and display an appropriate error message
4. WHEN an administrator uploads a file with an unsupported format THEN the Mandays Summary System SHALL reject the file and display a format error message

### Requirement 2

**User Story:** As an administrator, I want the system to validate mandatory fields in uploaded files, so that only complete and valid data is imported.

#### Acceptance Criteria

1. WHEN the Mandays Summary System processes an uploaded file THEN the Mandays Summary System SHALL validate that epNo, punchDate, mandays, regularMandayHr, and ot columns are present
2. WHEN the uploaded file is missing any mandatory column THEN the Mandays Summary System SHALL reject the file and display which mandatory columns are missing
3. WHEN any row contains an empty value for epNo THEN the Mandays Summary System SHALL reject that row and report the validation error
4. WHEN any row contains an empty value for punchDate THEN the Mandays Summary System SHALL reject that row and report the validation error
5. WHEN any row contains an empty value for mandays, regularMandayHr, or ot THEN the Mandays Summary System SHALL reject that row and report the validation error

### Requirement 3

**User Story:** As an administrator, I want the system to extract specific columns from uploaded files, so that only relevant data is stored in the system.

#### Acceptance Criteria

1. WHEN the Mandays Summary System processes a valid file THEN the Mandays Summary System SHALL extract epNo, punchDate, trade, skill, contract, plant, mandays, regularMandayHr, ot, and plantDesc columns
2. WHEN the uploaded file contains additional columns beyond the specified set THEN the Mandays Summary System SHALL ignore those columns
3. WHEN optional columns (trade, skill, contract, plant, plantDesc) are missing from a row THEN the Mandays Summary System SHALL store NULL or empty values for those fields
4. WHEN the Mandays Summary System extracts data THEN the Mandays Summary System SHALL preserve the data types for numeric fields (mandays, regularMandayHr, ot)

### Requirement 4

**User Story:** As an administrator, I want to see validation results after uploading a file, so that I can understand which records were successfully imported and which failed.

#### Acceptance Criteria

1. WHEN the Mandays Summary System completes file processing THEN the Mandays Summary System SHALL display the total number of rows processed
2. WHEN the Mandays Summary System completes file processing THEN the Mandays Summary System SHALL display the number of successfully imported records
3. WHEN validation errors occur THEN the Mandays Summary System SHALL display the number of failed records with specific error messages
4. WHEN validation errors occur THEN the Mandays Summary System SHALL display row numbers and error descriptions for each failed record
5. WHEN all records are successfully imported THEN the Mandays Summary System SHALL display a success confirmation message

### Requirement 5

**User Story:** As an administrator, I want the system to validate data types and formats, so that only correctly formatted data is stored.

#### Acceptance Criteria

1. WHEN the Mandays Summary System validates epNo THEN the Mandays Summary System SHALL accept alphanumeric employee numbers
2. WHEN the Mandays Summary System validates punchDate THEN the Mandays Summary System SHALL accept dates in standard formats (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY)
3. WHEN the Mandays Summary System validates mandays THEN the Mandays Summary System SHALL accept numeric values greater than or equal to zero
4. WHEN the Mandays Summary System validates regularMandayHr THEN the Mandays Summary System SHALL accept numeric values greater than or equal to zero
5. WHEN the Mandays Summary System validates ot THEN the Mandays Summary System SHALL accept numeric values greater than or equal to zero
6. WHEN any numeric field contains non-numeric data THEN the Mandays Summary System SHALL reject that row and report a data type error

### Requirement 6

**User Story:** As an administrator, I want to view and manage uploaded manday records, so that I can verify and correct data as needed.

#### Acceptance Criteria

1. WHEN an administrator accesses the mandays summary view THEN the Mandays Summary System SHALL display all imported manday records in a paginated table
2. WHEN displaying manday records THEN the Mandays Summary System SHALL show all extracted columns (epNo, punchDate, trade, skill, contract, plant, mandays, regularMandayHr, ot, plantDesc)
3. WHEN an administrator filters by date range THEN the Mandays Summary System SHALL display only records within the specified punchDate range
4. WHEN an administrator filters by employee number THEN the Mandays Summary System SHALL display only records matching the specified epNo
5. WHEN an administrator exports manday data THEN the Mandays Summary System SHALL generate a downloadable Excel file with all filtered records

### Requirement 7

**User Story:** As a system administrator, I want access controls on the mandays upload feature, so that only authorized users can import sensitive work data.

#### Acceptance Criteria

1. WHEN a user with USER1 role attempts to access the mandays upload page THEN the Mandays Summary System SHALL deny access and display an authorization error
2. WHEN a user with USER2 or USER3 role accesses the mandays upload page THEN the Mandays Summary System SHALL grant access to the upload functionality
3. WHEN an unauthenticated user attempts to access the mandays upload page THEN the Mandays Summary System SHALL redirect to the login page
