# Design Document: User1 Supervisor Management & Access Request System

## Overview

The User1 Supervisor Management system enables supervisors (User1 role) to manage and view attendance data for specific employees assigned to them. The system includes an access request workflow where User1 users can request access to employees, and Admin users approve or reject these requests with flexible date ranges. Additionally, the system provides visual highlighting for employees with excessive overstay (> 01:00 hours) to facilitate quick identification of overtime issues.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interfaces                           │
│  ┌──────────────────┐  ┌──────────────────────────────────┐│
│  │  User1 Views     │  │     Admin Views                  ││
│  │  - My Team       │  │     - Approve Requests           ││
│  │  - Request Access│  │     - Manage Assignments         ││
│  │  - My Requests   │  │     - Audit Logs                 ││
│  └──────────────────┘  └──────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         AccessControlService                          │  │
│  │  - check_employee_access()                            │  │
│  │  - get_assigned_employees()                           │  │
│  │  - filter_by_assignments()                            │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         RequestApprovalService                        │  │
│  │  - create_request()                                   │  │
│  │  - approve_request()                                  │  │
│  │  - reject_request()                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Models                             │
│  - EmployeeAssignment                                        │
│  - AccessRequest                                             │
│  - AccessRequestAuditLog                                     │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. EmployeeAssignment Model

Represents the assignment of an employee to a User1 supervisor.

```python
class EmployeeAssignment(models.Model):
    user = ForeignKey(User)  # User1 supervisor
    ep_no = CharField()  # Employee number
    ep_name = CharField()  # Employee name (cached for performance)
    company = ForeignKey(Company)
    
    # Date range (None = permanent access)
    access_from = DateField(null=True, blank=True)
    access_to = DateField(null=True, blank=True)
    
    # Metadata
    assigned_by = ForeignKey(User)  # Admin who assigned
    assigned_at = DateTimeField(auto_now_add=True)
    source = CharField(choices=['request', 'admin'])  # How it was created
    
    # Status
    is_active = BooleanField(default=True)
```

### 2. AccessRequest Model

Represents a request from User1 to access employee data.

```python
class AccessRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    ]
    
    ACCESS_TYPE_CHOICES = [
        ('date_range', 'Date Range'),
        ('permanent', 'Permanent')
    ]
    
    requester = ForeignKey(User)  # User1 who requested
    ep_no = CharField()  # Employee number
    company = ForeignKey(Company)
    
    # Access details
    access_type = CharField(choices=ACCESS_TYPE_CHOICES)
    access_from = DateField(null=True, blank=True)
    access_to = DateField(null=True, blank=True)
    justification = TextField()
    
    # Status
    status = CharField(choices=STATUS_CHOICES, default='pending')
    
    # Approval/Rejection
    reviewed_by = ForeignKey(User, null=True)  # Admin who reviewed
    reviewed_at = DateTimeField(null=True)
    rejection_reason = TextField(blank=True)
    
    # Timestamps
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

### 3. AccessControlService

Service for checking and filtering employee access.

```python
class AccessControlService:
    def check_employee_access(self, user, ep_no, date=None):
        """Check if user has access to employee on specific date"""
        
    def get_assigned_employees(self, user, date=None):
        """Get list of EP NOs user can access"""
        
    def filter_queryset_by_access(self, queryset, user):
        """Filter attendance queryset by user's assignments"""
        
    def is_assignment_active(self, assignment, check_date=None):
        """Check if assignment is currently active"""
```

### 4. RequestApprovalService

Service for managing access requests.

```python
class RequestApprovalService:
    def create_request(self, user, ep_nos, access_type, dates, justification):
        """Create access request(s)"""
        
    def approve_request(self, request_id, admin_user):
        """Approve request and create assignment"""
        
    def reject_request(self, request_id, admin_user, reason):
        """Reject request with reason"""
        
    def cancel_request(self, request_id, user):
        """Cancel pending request"""
```

## Data Models

### New Models

#### EmployeeAssignment
- Links User1 to specific employees (EP NO)
- Supports date range or permanent access
- Tracks who assigned and when
- Automatically expires based on date range

#### AccessRequest
- Stores User1 requests for employee access
- Supports bulk requests (multiple EP NOs)
- Tracks approval/rejection workflow
- Includes justification and rejection reason

#### AccessRequestAuditLog
- Logs all access-related events
- Tracks assignments, approvals, rejections, expirations
- Enables compliance and auditing

### Model Relationships

```
User (User1) ──┬─→ EmployeeAssignment ──→ Company
               │
               └─→ AccessRequest ──→ Company
                        │
                        └─→ reviewed_by (Admin User)
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Access Control Filtering
*For any* User1 user and any operation (view, search, export, statistics), all returned attendance records should belong only to employees assigned to that User1 user.
**Validates: Requirements 1.1, 1.2, 1.3, 1.5**

### Property 2: Overstay Highlighting
*For any* attendance record with overstay > 01:00 hours, the rendered output should include distinct visual highlighting (background color and bold red text).
**Validates: Requirements 2.1, 2.2**

### Property 3: Overstay Count Accuracy
*For any* set of attendance records, the count of employees with overstay > 01:00 should equal the number of records where overstay exceeds 01:00.
**Validates: Requirements 2.4**

### Property 4: Overstay Export Indicator
*For any* exported attendance data, records with overstay > 01:00 should include a visual indicator in the exported file.
**Validates: Requirements 2.5**

### Property 5: Request Validation Rules
*For any* access request, it should be valid if and only if: (1) it includes EP NO, access type, and justification, (2) date range requests include start and end dates, and (3) permanent requests do not require dates.
**Validates: Requirements 3.2, 3.3, 3.4**

### Property 6: New Request Initial Status
*For any* newly submitted access request, its status should be "pending".
**Validates: Requirements 3.5**

### Property 7: Pending Requests Visibility
*For any* admin user viewing the approval page, all pending access requests should be displayed.
**Validates: Requirements 4.1**

### Property 8: Request Detail Completeness
*For any* access request being reviewed, the displayed information should include requester name, EP NO, access type, date range (if applicable), and justification.
**Validates: Requirements 4.2**

### Property 9: Approval Creates Assignment
*For any* approved access request, an employee assignment should exist with matching User1, EP NO, and date range details.
**Validates: Requirements 4.3**

### Property 10: Rejection Updates Status
*For any* rejected access request, its status should be "rejected" and optionally include a rejection reason.
**Validates: Requirements 4.4**

### Property 11: User Sees Own Requests
*For any* User1 user viewing their requests, all displayed requests should belong to that user and no requests from other users should appear.
**Validates: Requirements 5.1**

### Property 12: Request Status Display
*For any* access request, the displayed information should include status-specific details: submission date for pending, approval date and date range for approved, rejection date and reason for rejected.
**Validates: Requirements 5.2, 5.3, 5.4**

### Property 13: Request History Sort Order
*For any* list of access requests, they should be sorted by creation timestamp in descending order (most recent first).
**Validates: Requirements 5.5**

### Property 14: Assignment Page Completeness
*For any* admin viewing the assignment page, all User1 users and their assignments should be displayed.
**Validates: Requirements 6.1**

### Property 15: Assignment Creation
*For any* valid assignment data (User1, EP NO, optional date range), the system should successfully create an employee assignment.
**Validates: Requirements 6.2**

### Property 16: Assignment Removal Revokes Access
*For any* employee assignment, after removal, the User1 should no longer have access to that employee's data.
**Validates: Requirements 6.3**

### Property 17: Automatic Assignment Expiration
*For any* employee assignment with an end date in the past, the assignment should not be active.
**Validates: Requirements 6.4**

### Property 18: Assignment Grouping
*For any* list of assignments, active assignments and expired assignments should be displayed in separate groups.
**Validates: Requirements 6.5**

### Property 19: Date Range Access Filtering
*For any* User1 with date-range assignment and any query date, employee data should be visible if and only if the query date falls within the assignment's date range (or assignment is permanent).
**Validates: Requirements 7.1, 7.4, 7.5**

### Property 20: Bulk Request Parsing
*For any* bulk access request with N EP NOs (comma-separated or line-by-line), the system should parse exactly N distinct EP NOs.
**Validates: Requirements 8.1**

### Property 21: Bulk Request Consistency
*For any* bulk access request with multiple EP NOs, all created individual requests should have identical access type, date range, and justification.
**Validates: Requirements 8.2**

### Property 22: Bulk Request Splitting
*For any* bulk access request with N EP NOs, exactly N individual access requests should be created.
**Validates: Requirements 8.3**

### Property 23: Invalid EP NO Validation
*For any* bulk access request containing invalid EP NOs, the system should display validation errors specifically identifying each invalid EP NO.
**Validates: Requirements 8.5**

### Property 24: Audit Log Completeness
*For any* access request or assignment change, a corresponding audit log entry should exist with timestamp and actor information.
**Validates: Requirements 9.1, 9.2, 9.5**

### Property 25: Audit Log Filtering
*For any* audit log query with filters (User1, EP NO, date range, action type), all returned results should match the filter criteria.
**Validates: Requirements 9.3**

### Property 26: Audit Log Export Completeness
*For any* exported audit log, all relevant details (timestamp, actor, action, target, details) should be included.
**Validates: Requirements 9.4**

### Property 27: Assignment Count Accuracy
*For any* User1 user, the displayed count of assigned employees should equal the number of active assignments for that user.
**Validates: Requirements 10.1**

### Property 28: Assignment Summary Completeness
*For any* User1 user's assignment summary, all assigned EP NOs with names and source information should be displayed.
**Validates: Requirements 10.2, 10.5**

### Property 29: Days Until Expiration Calculation
*For any* assignment with a future end date, the displayed days remaining should equal the difference between the end date and current date.
**Validates: Requirements 10.3**

### Property 30: Expiration Warning Highlighting
*For any* assignment with an end date within 7 days, the display should include a warning indicator.
**Validates: Requirements 10.4**



## Error Handling

### Access Denied Scenarios

1. **Unauthorized Employee Access**
   - When: User1 attempts to access employee not assigned to them
   - Response: Return 403 Forbidden with clear message
   - Logging: Log unauthorized access attempt with user and EP NO

2. **Expired Assignment Access**
   - When: User1 attempts to access employee with expired assignment
   - Response: Display message indicating access has expired
   - Action: Suggest requesting new access

3. **Invalid Date Range**
   - When: Assignment or request has end date before start date
   - Response: Validation error with specific message
   - Prevention: Client-side validation before submission

### Request Processing Errors

1. **Invalid EP NO**
   - When: Request contains non-existent employee number
   - Response: Validation error identifying invalid EP NO
   - Handling: For bulk requests, show all invalid EP NOs

2. **Duplicate Request**
   - When: User1 submits request for employee they already have access to
   - Response: Warning message with option to proceed or cancel
   - Handling: Allow request if date range differs

3. **Request Not Found**
   - When: Attempting to approve/reject non-existent request
   - Response: 404 Not Found with clear message
   - Logging: Log the attempted action

### Data Integrity Errors

1. **Concurrent Modification**
   - When: Two admins approve/reject same request simultaneously
   - Response: Show error to second admin indicating request already processed
   - Prevention: Use database transactions and optimistic locking

2. **Assignment Conflict**
   - When: Creating assignment that overlaps with existing assignment
   - Response: Warning message showing existing assignment
   - Handling: Allow admin to proceed or adjust date range

3. **Missing Required Data**
   - When: Form submission missing required fields
   - Response: Validation errors highlighting missing fields
   - Prevention: Client-side validation with clear field labels

### System Errors

1. **Database Connection Failure**
   - Response: User-friendly error message
   - Logging: Log full error details for debugging
   - Recovery: Retry logic for transient failures

2. **Notification Failure**
   - Response: Complete the primary action (approve/reject)
   - Logging: Log notification failure separately
   - Recovery: Background job to retry failed notifications

## Testing Strategy

### Unit Testing

Unit tests will verify specific examples, edge cases, and component behavior:

**Access Control Tests:**
- Test User1 with no assignments sees empty list
- Test User1 with single assignment sees only that employee
- Test expired assignment does not grant access
- Test future assignment does not grant current access

**Request Validation Tests:**
- Test date range request without dates is rejected
- Test permanent request with dates is accepted (dates ignored)
- Test request with invalid EP NO is rejected
- Test bulk request parsing with various formats

**Approval Workflow Tests:**
- Test approving request creates assignment
- Test rejecting request updates status
- Test cancelling pending request
- Test cannot approve already-processed request

**Date Range Logic Tests:**
- Test assignment active on start date
- Test assignment inactive on day after end date
- Test permanent assignment has no date restrictions
- Test date filter intersection with assignment range

**Overstay Highlighting Tests:**
- Test overstay of 00:59 is not highlighted
- Test overstay of 01:00 is highlighted
- Test overstay of 01:01 is highlighted
- Test null overstay is not highlighted

### Property-Based Testing

Property-based tests will verify universal properties across all inputs using **Hypothesis** (Python's PBT library):

**Configuration:**
- Minimum 100 iterations per property test
- Each test tagged with format: `# Feature: user1-supervisor-management, Property N: [property text]`

**Core Properties to Test:**

1. **Property 1: Access Control Filtering** - Generate random User1 users with random assignments and attendance data, verify filtered results contain only assigned employees

2. **Property 5: Request Validation Rules** - Generate random request data with various combinations of fields, verify validation accepts/rejects correctly

3. **Property 9: Approval Creates Assignment** - Generate random pending requests, approve them, verify assignments exist with matching details

4. **Property 16: Assignment Removal Revokes Access** - Generate random assignments, remove them, verify access is revoked

5. **Property 19: Date Range Access Filtering** - Generate random assignments with date ranges and query dates, verify visibility follows date range rules

6. **Property 21: Bulk Request Consistency** - Generate random bulk requests, verify all individual requests have identical parameters

7. **Property 22: Bulk Request Splitting** - Generate random bulk requests with N EP NOs, verify exactly N requests created

8. **Property 24: Audit Log Completeness** - Generate random access events, verify all appear in audit log

9. **Property 27: Assignment Count Accuracy** - Generate random User1 users with various assignments, verify count matches active assignments

10. **Property 29: Days Until Expiration Calculation** - Generate random assignments with future end dates, verify days remaining calculation

**Generator Strategies:**
- User1 users with random usernames and companies
- EP NOs as valid employee identifiers
- Date ranges with start < end constraint
- Access types from valid choices
- Request statuses from valid choices
- Overstay values from 00:00 to 05:00 hours

### Integration Testing

Integration tests will verify end-to-end workflows:

1. **Request-to-Assignment Flow**
   - User1 submits request → Admin approves → Assignment created → User1 can access employee

2. **Bulk Request Processing**
   - User1 submits bulk request → Multiple individual requests created → Admin approves all → Multiple assignments created

3. **Assignment Expiration**
   - Create assignment with end date → Advance time past end date → Verify access revoked → Verify audit log entry

4. **Access Control Enforcement**
   - User1 with assignments → Attempt to access unassigned employee → Verify 403 error → Verify audit log

5. **Dashboard Statistics**
   - Create assignments and attendance data → View dashboard → Verify counts and statistics match

### Test Coverage Goals

- Unit test coverage: >80% of service and model code
- Property test coverage: All 30 correctness properties
- Integration test coverage: All major user workflows
- Edge case coverage: Empty states, boundary dates, invalid inputs

### Testing Tools

- **pytest**: Test runner and framework
- **Hypothesis**: Property-based testing library
- **pytest-django**: Django integration for pytest
- **factory_boy**: Test data generation
- **freezegun**: Time manipulation for date-based tests
