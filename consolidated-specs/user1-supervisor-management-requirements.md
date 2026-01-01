# Requirements Document

## Introduction

This document specifies requirements for the User1 Supervisor Management and Access Request System. The system enables User1 users (supervisors/managers) to view attendance data only for employees they manage, request access to additional employees, and easily identify employees with excessive overstay hours.

## Glossary

- **User1**: A user with role='user1' representing a supervisor or manager
- **Admin**: A user with role='admin' who can approve access requests
- **Root**: A user with role='root' with full system access
- **EP NO**: Employee Number - unique identifier for each employee
- **Overstay**: Hours worked beyond scheduled shift time
- **Access Request**: A request from User1 to view specific employee's attendance data
- **Access Assignment**: Approved permission for User1 to view employee data
- **Date Range Access**: Time-limited access to employee data (from date to date)
- **Permanent Access**: Unlimited access to employee data

## Requirements

### Requirement 1

**User Story:** As a User1 supervisor, I want to see only attendance data for employees assigned to me, so that I can focus on managing my team without seeing irrelevant data.

#### Acceptance Criteria

1. WHEN a User1 user logs in and views attendance list THEN the system SHALL display only records for employees assigned to that User1
2. WHEN a User1 user searches for attendance THEN the system SHALL search only within their assigned employees
3. WHEN a User1 user exports data THEN the system SHALL export only their assigned employees' records
4. WHEN a User1 user has no assigned employees THEN the system SHALL display an empty list with a message
5. WHEN a User1 user views dashboard statistics THEN the system SHALL calculate statistics only for their assigned employees

### Requirement 2

**User Story:** As a User1 supervisor, I want to easily identify employees with overstay exceeding 01:00 hours, so that I can quickly spot overtime issues and take action.

#### Acceptance Criteria

1. WHEN displaying attendance records with overstay > 01:00 THEN the system SHALL highlight the entire row with a distinct background color
2. WHEN displaying overstay value > 01:00 THEN the system SHALL display the value in bold red text
3. WHEN a User1 user filters attendance list THEN the system SHALL provide a quick filter option for "Overstay > 1 hour"
4. WHEN displaying dashboard for User1 THEN the system SHALL show count of employees with overstay > 01:00
5. WHEN exporting data THEN the system SHALL include a visual indicator for overstay > 01:00 in exported files

### Requirement 3

**User Story:** As a User1 supervisor, I want to request access to view specific employees' attendance data, so that I can manage temporary team members or cross-functional workers.

#### Acceptance Criteria

1. WHEN a User1 user accesses the request page THEN the system SHALL display a form to request employee access
2. WHEN submitting an access request THEN the system SHALL require EP NO, access type (date range or permanent), and justification
3. WHEN requesting date range access THEN the system SHALL require start date and end date
4. WHEN requesting permanent access THEN the system SHALL not require date fields
5. WHEN a request is submitted THEN the system SHALL save it with status "pending" and notify admin users

### Requirement 4

**User Story:** As an Admin user, I want to review and approve/reject User1 access requests, so that I can control which employees each supervisor can view.

#### Acceptance Criteria

1. WHEN an Admin user accesses the approval page THEN the system SHALL display all pending access requests
2. WHEN reviewing a request THEN the system SHALL show requester name, EP NO, access type, date range, and justification
3. WHEN approving a request THEN the system SHALL create an employee assignment for that User1
4. WHEN rejecting a request THEN the system SHALL mark it as rejected and optionally add rejection reason
5. WHEN a request is approved or rejected THEN the system SHALL notify the requesting User1

### Requirement 5

**User Story:** As a User1 supervisor, I want to see the status of my access requests, so that I know which requests are pending, approved, or rejected.

#### Acceptance Criteria

1. WHEN a User1 user views their requests THEN the system SHALL display all requests with status (pending, approved, rejected)
2. WHEN a request is pending THEN the system SHALL show submission date and allow cancellation
3. WHEN a request is approved THEN the system SHALL show approval date and assigned date range
4. WHEN a request is rejected THEN the system SHALL show rejection date and reason
5. WHEN viewing request history THEN the system SHALL sort by most recent first

### Requirement 6

**User Story:** As an Admin user, I want to manage employee assignments for User1 users, so that I can directly assign or remove employee access without requiring requests.

#### Acceptance Criteria

1. WHEN an Admin user accesses employee assignment page THEN the system SHALL display all User1 users and their assignments
2. WHEN adding an assignment THEN the system SHALL allow selecting User1, EP NO, and optional date range
3. WHEN removing an assignment THEN the system SHALL revoke User1 access to that employee
4. WHEN an assignment has a date range THEN the system SHALL automatically revoke access after end date
5. WHEN viewing assignments THEN the system SHALL show active and expired assignments separately

### Requirement 7

**User Story:** As a User1 supervisor, I want my employee assignments to respect date ranges, so that I only see data for employees during the period I'm managing them.

#### Acceptance Criteria

1. WHEN a User1 has date-range assignment THEN the system SHALL show employee data only within that date range
2. WHEN current date is before assignment start date THEN the system SHALL not show that employee's data
3. WHEN current date is after assignment end date THEN the system SHALL not show that employee's data
4. WHEN a User1 has permanent assignment THEN the system SHALL show all historical and future data for that employee
5. WHEN filtering by date THEN the system SHALL respect both filter dates and assignment date ranges

### Requirement 8

**User Story:** As a User1 supervisor, I want to request access for multiple employees at once, so that I can efficiently manage access for my entire team.

#### Acceptance Criteria

1. WHEN submitting an access request THEN the system SHALL allow entering multiple EP NOs (comma-separated or line-by-line)
2. WHEN requesting multiple employees THEN the system SHALL apply the same access type and date range to all
3. WHEN processing bulk request THEN the system SHALL create individual requests for each EP NO
4. WHEN approving bulk request THEN the system SHALL allow approving all or individual employees
5. WHEN any EP NO is invalid THEN the system SHALL show validation error for that specific EP NO

### Requirement 9

**User Story:** As an Admin user, I want to see audit logs of all access requests and assignments, so that I can track who has access to which employees and when.

#### Acceptance Criteria

1. WHEN viewing audit logs THEN the system SHALL display all access requests with timestamps
2. WHEN viewing audit logs THEN the system SHALL display all assignment changes with who made the change
3. WHEN filtering audit logs THEN the system SHALL allow filtering by User1, EP NO, date range, and action type
4. WHEN exporting audit logs THEN the system SHALL include all relevant details in the export
5. WHEN an assignment expires THEN the system SHALL log the automatic expiration event

### Requirement 10

**User Story:** As a User1 supervisor, I want to see a summary of my current employee assignments, so that I know which employees I can view and when my access expires.

#### Acceptance Criteria

1. WHEN a User1 user views their dashboard THEN the system SHALL display count of assigned employees
2. WHEN viewing assignment summary THEN the system SHALL show list of assigned EP NOs with names
3. WHEN an assignment has expiration date THEN the system SHALL show days remaining until expiration
4. WHEN an assignment is expiring soon (within 7 days) THEN the system SHALL highlight it with a warning
5. WHEN viewing assignment details THEN the system SHALL show assignment source (request or admin-assigned)
