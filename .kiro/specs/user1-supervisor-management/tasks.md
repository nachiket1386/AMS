# Implementation Plan

- [x] 1. Create data models and migrations

- [x] 1.1 Create EmployeeAssignment model



  - Define model with fields: user, ep_no, ep_name, company, access_from, access_to, assigned_by, assigned_at, source, is_active
  - Add model methods: is_active_on_date(), get_date_range_display()


  - _Requirements: 1.1, 6.2, 6.4, 7.1_

- [x] 1.2 Create AccessRequest model


  - Define model with fields: requester, ep_no, company, access_type, access_from, access_to, justification, status, reviewed_by, reviewed_at, rejection_reason
  - Add model methods: can_cancel(), can_approve(), can_reject()
  - _Requirements: 3.2, 3.3, 3.4, 4.3, 4.4_



- [x] 1.3 Create AccessRequestAuditLog model

  - Define model with fields: timestamp, actor, action, target_user, target_ep_no, details


  - Add model method: create_log_entry()
  - _Requirements: 9.1, 9.2, 9.5_



- [x] 1.4 Generate and apply database migrations

  - Create migrations for all three models



  - Apply migrations to database
  - _Requirements: All data model requirements_

- [x] 1.5 Write property test for assignment date range logic


  - **Property 17: Automatic Assignment Expiration**
  - **Validates: Requirements 6.4**






- [x] 1.6 Write property test for request validation

  - **Property 5: Request Validation Rules**
  - **Validates: Requirements 3.2, 3.3, 3.4**

- [x] 2. Implement AccessControlService



- [x] 2.1 Create AccessControlService class

  - Implement check_employee_access(user, ep_no, date) method
  - Implement get_assigned_employees(user, date) method
  - Implement filter_queryset_by_access(queryset, user) method
  - Implement is_assignment_active(assignment, check_date) method

  - _Requirements: 1.1, 1.2, 1.3, 7.1, 7.4, 7.5_

- [x] 2.2 Write property test for access control filtering

  - **Property 1: Access Control Filtering**


  - **Validates: Requirements 1.1, 1.2, 1.3, 1.5**



- [x] 2.3 Write property test for date range filtering

  - **Property 19: Date Range Access Filtering**

  - **Validates: Requirements 7.1, 7.4, 7.5**

- [x] 2.4 Write unit tests for AccessControlService



  - Test User1 with no assignments sees empty list
  - Test expired assignment does not grant access
  - Test future assignment does not grant current access
  - _Requirements: 1.1, 1.4, 7.2, 7.3_

- [x] 3. Implement RequestApprovalService



- [x] 3.1 Create RequestApprovalService class


  - Implement create_request(user, ep_nos, access_type, dates, justification) method
  - Implement approve_request(request_id, admin_user) method
  - Implement reject_request(request_id, admin_user, reason) method

  - Implement cancel_request(request_id, user) method
  - _Requirements: 3.2, 3.5, 4.3, 4.4, 5.2_

- [x] 3.2 Add audit logging to RequestApprovalService

  - Log request creation, approval, rejection, cancellation events

  - Include actor, timestamp, and relevant details
  - _Requirements: 9.1, 9.2, 9.5_


- [x] 3.3 Write property test for approval creates assignment


  - **Property 9: Approval Creates Assignment**
  - **Validates: Requirements 4.3**


- [x] 3.4 Write property test for rejection updates status

  - **Property 10: Rejection Updates Status**

  - **Validates: Requirements 4.4**

- [x] 3.5 Write property test for audit log completeness

  - **Property 24: Audit Log Completeness**


  - **Validates: Requirements 9.1, 9.2, 9.5**

- [x] 3.6 Write unit tests for RequestApprovalService


  - Test cannot approve already-processed request

  - Test cancelling pending request
  - Test duplicate request handling
  - _Requirements: 3.5, 4.3, 4.4_

- [x] 4. Implement bulk request processing

- [x] 4.1 Add bulk EP NO parsing to RequestApprovalService


  - Parse comma-separated and line-by-line EP NO formats
  - Validate each EP NO
  - Return list of valid and invalid EP NOs
  - _Requirements: 8.1, 8.5_

- [x] 4.2 Implement bulk request creation logic

  - Create individual requests for each valid EP NO
  - Apply same access type, date range, and justification to all
  - Handle validation errors for invalid EP NOs
  - _Requirements: 8.2, 8.3, 8.5_

- [x] 4.3 Write property test for bulk request parsing


  - **Property 20: Bulk Request Parsing**
  - **Validates: Requirements 8.1**

- [x] 4.4 Write property test for bulk request consistency

  - **Property 21: Bulk Request Consistency**
  - **Validates: Requirements 8.2**

- [x] 4.5 Write property test for bulk request splitting

  - **Property 22: Bulk Request Splitting**
  - **Validates: Requirements 8.3**

- [x] 4.6 Write property test for invalid EP NO validation

  - **Property 23: Invalid EP NO Validation**
  - **Validates: Requirements 8.5**

- [x] 5. Update attendance views with access control

- [x] 5.1 Modify attendance_list view


  - Add AccessControlService filtering for User1 users
  - Keep existing functionality for Admin and Root users
  - Handle empty assignment case with appropriate message
  - _Requirements: 1.1, 1.4_

- [x] 5.2 Modify attendance search functionality

  - Apply access control filtering to search results
  - Ensure User1 only searches within assigned employees
  - _Requirements: 1.2_

- [x] 5.3 Modify attendance export functionality



  - Apply access control filtering to export data
  - Ensure User1 only exports assigned employees' records
  - _Requirements: 1.3_

- [x] 5.4 Modify dashboard statistics



  - Apply access control filtering to statistics calculations
  - Calculate statistics only for assigned employees
  - _Requirements: 1.5_

- [x] 5.5 Write integration test for access control enforcement


  - Test User1 with assignments can access assigned employees
  - Test User1 cannot access unassigned employees
  - Test Admin and Root have full access
  - _Requirements: 1.1, 1.2, 1.3, 1.5_

- [x] 6. Implement overstay highlighting

- [x] 6.1 Add overstay highlighting to attendance_list template



  - Add CSS class for rows with overstay > 01:00
  - Style overstay values > 01:00 in bold red
  - Add distinct background color for highlighted rows
  - _Requirements: 2.1, 2.2_

- [x] 6.2 Add overstay quick filter


  - Add filter button/option for "Overstay > 1 hour"
  - Filter attendance list to show only records with overstay > 01:00
  - _Requirements: 2.3_

- [x] 6.3 Add overstay count to User1 dashboard


  - Calculate count of employees with overstay > 01:00
  - Display count prominently on dashboard
  - _Requirements: 2.4_


- [x] 6.4 Add overstay indicator to export

  - Include visual indicator (e.g., asterisk, flag) for overstay > 01:00 in CSV/Excel exports
  - _Requirements: 2.5_

- [x] 6.5 Write property test for overstay highlighting


  - **Property 2: Overstay Highlighting**
  - **Validates: Requirements 2.1, 2.2**

- [x] 6.6 Write property test for overstay count accuracy


  - **Property 3: Overstay Count Accuracy**
  - **Validates: Requirements 2.4**

- [x] 6.7 Write unit tests for overstay features



  - Test overstay of 00:59 is not highlighted
  - Test overstay of 01:00 is highlighted
  - Test overstay of 01:01 is highlighted
  - _Requirements: 2.1, 2.2_

- [x] 7. Create User1 request access interface

- [x] 7.1 Create request_access view and template



  - Display form with EP NO input (support multiple), access type, date range, justification
  - Validate form inputs according to access type
  - Handle bulk EP NO parsing
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 8.1_

- [x] 7.2 Implement request submission logic


  - Create access request(s) with status "pending"
  - Handle bulk requests by creating individual requests
  - Show validation errors for invalid EP NOs
  - Display success message with request count
  - _Requirements: 3.5, 8.2, 8.3, 8.5_

- [x] 7.3 Create my_requests view and template


  - Display all requests for logged-in User1
  - Show status, submission date, and status-specific details
  - Sort by most recent first
  - Allow cancellation of pending requests
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 7.4 Write property test for user sees own requests


  - **Property 11: User Sees Own Requests**
  - **Validates: Requirements 5.1**

- [x] 7.5 Write property test for request history sort order


  - **Property 13: Request History Sort Order**
  - **Validates: Requirements 5.5**

- [x] 8. Create Admin approval interface

- [x] 8.1 Create approve_requests view and template



  - Display all pending access requests
  - Show requester name, EP NO, access type, date range, justification
  - Provide approve and reject actions for each request
  - _Requirements: 4.1, 4.2_

- [x] 8.2 Implement approval action


  - Approve request and create employee assignment
  - Update request status to "approved"
  - Log approval event in audit log
  - _Requirements: 4.3, 9.2_

- [x] 8.3 Implement rejection action


  - Reject request with optional reason
  - Update request status to "rejected"
  - Log rejection event in audit log
  - _Requirements: 4.4, 9.2_

- [x] 8.4 Write property test for pending requests visibility


  - **Property 7: Pending Requests Visibility**
  - **Validates: Requirements 4.1**

- [x] 8.5 Write property test for request detail completeness


  - **Property 8: Request Detail Completeness**
  - **Validates: Requirements 4.2**

- [x] 9. Create Admin assignment management interface

- [x] 9.1 Create manage_assignments view and template


  - Display all User1 users and their assignments
  - Show active and expired assignments separately
  - Provide add and remove assignment actions
  - _Requirements: 6.1, 6.5_

- [x] 9.2 Implement add assignment action


  - Allow selecting User1, EP NO, and optional date range
  - Create employee assignment with source "admin"
  - Log assignment creation in audit log
  - _Requirements: 6.2, 9.2_

- [x] 9.3 Implement remove assignment action


  - Mark assignment as inactive
  - Verify User1 no longer has access to employee
  - Log assignment removal in audit log
  - _Requirements: 6.3, 9.2_

- [x] 9.4 Write property test for assignment removal revokes access


  - **Property 16: Assignment Removal Revokes Access**
  - **Validates: Requirements 6.3**

- [x] 9.5 Write property test for assignment grouping


  - **Property 18: Assignment Grouping**
  - **Validates: Requirements 6.5**

- [x] 10. Implement User1 dashboard enhancements

- [x] 10.1 Create assignment summary section


  - Display count of assigned employees
  - Show list of assigned EP NOs with names
  - Show assignment source (request or admin-assigned)
  - _Requirements: 10.1, 10.2, 10.5_

- [x] 10.2 Add expiration warnings


  - Calculate days remaining until expiration for each assignment
  - Highlight assignments expiring within 7 days with warning
  - _Requirements: 10.3, 10.4_

- [x] 10.3 Write property test for assignment count accuracy


  - **Property 27: Assignment Count Accuracy**
  - **Validates: Requirements 10.1**

- [x] 10.4 Write property test for days until expiration calculation


  - **Property 29: Days Until Expiration Calculation**
  - **Validates: Requirements 10.3**

- [x] 10.5 Write property test for expiration warning highlighting


  - **Property 30: Expiration Warning Highlighting**
  - **Validates: Requirements 10.4**

- [x] 11. Create audit log interface

- [x] 11.1 Create audit_logs view and template


  - Display all access requests and assignment changes
  - Show timestamp, actor, action, target, and details
  - Implement filtering by User1, EP NO, date range, and action type
  - _Requirements: 9.1, 9.2, 9.3_

- [x] 11.2 Implement audit log export


  - Export audit logs to CSV with all relevant details
  - Apply current filters to export
  - _Requirements: 9.4_

- [x] 11.3 Write property test for audit log filtering


  - **Property 25: Audit Log Filtering**
  - **Validates: Requirements 9.3**

- [x] 11.4 Write property test for audit log export completeness


  - **Property 26: Audit Log Export Completeness**
  - **Validates: Requirements 9.4**

- [x] 12. Add URL routing and navigation

- [x] 12.1 Add URL patterns for all new views



  - Add routes for request_access, my_requests, approve_requests, manage_assignments, audit_logs
  - Ensure proper URL namespacing
  - _Requirements: All view requirements_

- [x] 12.2 Update navigation menu


  - Add User1-specific menu items (My Team, Request Access, My Requests)
  - Add Admin-specific menu items (Approve Requests, Manage Assignments, Audit Logs)
  - Show/hide menu items based on user role
  - _Requirements: All view requirements_

- [x] 13. Implement automatic assignment expiration

- [x] 13.1 Create management command for expiration check


  - Check all assignments with end_date < today
  - Mark expired assignments as inactive
  - Log expiration events in audit log
  - _Requirements: 6.4, 9.5_

- [x] 13.2 Schedule expiration check as daily task


  - Configure task to run daily (e.g., via cron or Django-Q)
  - _Requirements: 6.4_

- [x] 13.3 Write integration test for assignment expiration


  - Create assignment with past end date
  - Run expiration check
  - Verify assignment is inactive and audit log entry exists
  - _Requirements: 6.4, 9.5_

- [x] 14. Add permission decorators and middleware


- [x] 14.1 Create permission decorators


  - Create @user1_required decorator for User1-only views
  - Create @admin_required decorator for Admin-only views
  - Apply decorators to all new views
  - _Requirements: All access control requirements_

- [x] 14.2 Add access control to existing views


  - Apply AccessControlService filtering to all attendance-related views
  - Ensure consistent access control across the application
  - _Requirements: 1.1, 1.2, 1.3, 1.5_

- [x] 15. Checkpoint - Ensure all tests pass





  - Ensure all tests pass, ask the user if questions arise.
