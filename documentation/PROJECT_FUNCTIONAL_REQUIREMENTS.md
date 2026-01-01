# 📋 Attendance Management System - Functional Requirements

## Project Overview

**Project Name:** Attendance Management System (AMS)  
**Technology Stack:** Django 4.2.7, Python 3.11, SQLite Database  
**Architecture:** Multi-tenant Web Application with Role-Based Access Control  
**Current Status:** Production-ready with 96,315 attendance records and 37,086 mandays records

---

## 1. User Authentication & Authorization

### 1.1 User Login
- Users can log in with username and password
- System authenticates credentials against database
- Successful login redirects to dashboard
- Failed login shows error message
- Already authenticated users are redirected to dashboard

### 1.2 User Logout
- Users can log out from any page
- System clears session and authentication tokens
- Logout action is logged in system logs
- User is redirected to login page with success message

### 1.3 Role-Based Access Control (RBAC)
The system supports three user roles with different permissions:

#### **ROOT User**
- Full system access across all companies
- Can view and manage all data
- Can create, edit, and delete users
- Can perform backup and restore operations
- Can delete all attendance records and companies
- Can view upload logs from all users
- Access to all administrative functions

#### **ADMIN User**
- Company-level access (restricted to assigned company)
- Can upload attendance and mandays CSV files
- Can view, edit, and delete attendance records for their company
- Can create and manage users within their company
- Can approve/reject access requests from User1
- Can manage employee assignments for User1 supervisors
- Can view upload logs for their company

#### **USER1 (Supervisor)**
- Limited employee-level access
- Can only view attendance data for assigned employees
- Access controlled by date ranges (optional)
- Can request access to additional employees
- Can view their own access requests
- Can cancel pending requests
- Cannot upload data or perform administrative tasks

---

## 2. Dashboard

### 2.1 Dashboard Statistics
- Displays total attendance records count
- Shows total companies count
- Lists recent 5 upload operations
- Statistics filtered based on user role:
  - **Root:** All records across all companies
  - **Admin:** Records for their company only
  - **User1:** Records for assigned employees only

### 2.2 Navigation
- Quick access to all major features
- Role-based menu items (only show accessible features)
- Responsive design for mobile and desktop
- User profile display with role badge

---

## 3. Attendance Management

### 3.1 View Attendance Records
- Paginated list view (50 records per page)
- Displays: Employee Number, Name, Company, Date, Shift, IN/OUT times, Status, Overstay, Overtime
- Data filtered by user role and permissions
- Responsive card layout for mobile devices
- Table layout for desktop devices

### 3.2 Filter Attendance Records
Users can filter attendance records by:
- **Date Range:** From date and To date
- **Employee Number:** Search by EP NO
- **Company:** (Root users only)
- **Status:** Present (P), Absent (A), Public Holiday (PH), Week Off (WO), Half Day (-0.5), Full Day Leave (-1)
- **Overstay Filters:**
  - Has Overstay (any overstay time)
  - No Overstay (00:00 or empty)
  - 1-2 hours overstay
  - 2-3 hours overstay
  - 3-4 hours overstay
  - Greater than 4 hours overstay

### 3.3 Edit Attendance Record
- Root and Admin users can edit records
- Admin users can only edit records from their company
- Edit form includes all attendance fields
- Changes are saved to database
- Success message displayed after update

### 3.4 Delete Attendance Record
- Root and Admin users can delete records
- Admin users can only delete records from their company
- Confirmation required before deletion
- Success message displayed after deletion

### 3.5 Delete All Records (Root Only)
- Root user can delete all attendance records
- Root user can delete all companies
- Confirmation required
- Action is logged in system logs

### 3.6 Export Attendance Data
- Export filtered records to Excel (XLSX format)
- Applies same filters as list view
- Includes all attendance fields
- Formatted with headers and styling
- Auto-adjusted column widths
- Filename includes timestamp

---

## 4. Attendance Data Upload

### 4.1 CSV/Excel Upload
- Root and Admin users can upload attendance data
- Supported formats: CSV, XLS, XLSX
- File validation before processing
- Progress tracking during upload
- Batch processing for large files

### 4.2 Upload Processing
- Parses CSV/Excel files
- Validates data format and required fields
- Creates new attendance records
- Updates existing records (based on EP NO + Date)
- Handles multiple time formats
- Extracts company information from data
- Creates companies automatically if not exist

### 4.3 Upload Results
- Displays success count (new records created)
- Displays updated count (existing records updated)
- Displays error count (failed records)
- Shows first 5 error messages
- Creates upload log entry
- All actions logged in system logs

### 4.4 Upload Logs
- View history of all uploads
- Shows: Filename, User, Timestamp, Success/Updated/Error counts
- Root users see all uploads
- Admin users see uploads for their company
- Paginated list view

### 4.5 Download CSV Template
- Provides sample CSV template for uploads
- Includes all required columns
- Helps users format data correctly

---

## 5. Mandays & Overtime Management

### 5.1 View Mandays Records
- Paginated list view (50 records per page)
- Displays: Employee Number, Date, Company, Mandays, OT (Overtime), Regular Hours, Trade, Contract, Plant
- OT displayed as decimal (e.g., 3.00, 4.50)
- Data filtered by user role and permissions
- Responsive card layout for mobile
- Table layout for desktop

### 5.2 Filter Mandays Records
Users can filter mandays records by:
- **Date Range:** From date and To date
- **Employee Number:** Search by EP NO
- **Company:** (Root users only)

### 5.3 Upload Mandays Data
- Root and Admin users can upload mandays CSV/Excel files
- Supported formats: CSV, XLS, XLSX
- Validates data format
- Creates/updates mandays records
- Converts OT from time format to decimal
- Creates upload log entry

### 5.4 Export Mandays Data
- Export filtered records to Excel (XLSX format)
- Applies same filters as list view
- Includes all mandays fields
- Formatted with headers and styling
- Filename includes timestamp

---

## 6. User Management

### 6.1 View Users
- List all users in the system
- Root users see all users
- Admin users see users in their company
- Displays: Username, Role, Company, Status
- Paginated list view

### 6.2 Create User
- Root and Admin users can create new users
- Required fields: Username, Password, Role, Company (for Admin/User1)
- Optional fields: Email, First Name, Last Name
- Date range access for User1 (optional)
- Password validation
- Role validation (Admin/User1 must have company)

### 6.3 Edit User
- Root and Admin users can edit users
- Admin users can only edit users in their company
- Can update: Username, Email, Role, Company, Date ranges
- Cannot edit Root users (except by Root)
- Password change optional

### 6.4 Delete User
- Root users only can delete users
- Cannot delete self
- Confirmation required
- Related data handled appropriately

---

## 7. Access Control System (User1 Supervisor)

### 7.1 Request Employee Access
- User1 can request access to specific employees
- Required fields:
  - Employee Number (EP NO)
  - Access Type (Date Range or Permanent)
  - Date Range (if Date Range type)
  - Justification (reason for access)
- System validates:
  - Employee exists in company
  - Date range is valid (from < to)
  - No duplicate pending requests
- Request status: Pending
- Request logged in audit trail

### 7.2 View My Requests
- User1 can view all their access requests
- Shows: Employee Number, Access Type, Date Range, Status, Justification
- Displays: Pending, Approved, Rejected, Cancelled requests
- Can cancel pending requests
- Paginated list view

### 7.3 Cancel Request
- User1 can cancel their own pending requests
- Only pending requests can be cancelled
- Status changed to "Cancelled"
- Action logged in audit trail
- Success message displayed

### 7.4 Approve Requests (Admin)
- Admin and Root users can approve access requests
- View all pending requests for their company
- Can approve or reject requests
- Approval creates employee assignment
- Rejection requires reason
- Action logged in audit trail
- Requester notified via message

### 7.5 Reject Requests (Admin)
- Admin and Root users can reject access requests
- Must provide rejection reason
- Status changed to "Rejected"
- Action logged in audit trail
- Requester notified via message

### 7.6 Manage Employee Assignments
- Admin and Root users can manage assignments
- View all active assignments
- Can create manual assignments (without request)
- Can remove assignments
- Can set date ranges for access
- Can make assignments permanent
- Shows: User1, Employee Number, Employee Name, Date Range, Source (Request/Admin)

### 7.7 Remove Assignment
- Admin and Root users can remove assignments
- Confirmation required
- Assignment marked as inactive
- Action logged in audit trail
- Success message displayed

### 7.8 Access Control Enforcement
- User1 can only view data for assigned employees
- Date range validation on data access
- Expired assignments automatically denied
- Permanent assignments have no date restrictions
- Access checked on every data query

---

## 8. Backup & Restore (Root Only)

### 8.1 Create Backup
- Root users can create full database backup
- Backup includes:
  - All companies
  - All attendance records
  - All mandays records
  - All users (except passwords)
  - All access requests and assignments
- Backup format: JSON
- Backup filename includes timestamp
- Backup log created with statistics

### 8.2 Download Backup
- Root users can download backup file
- File served as JSON download
- Filename: `backup_YYYYMMDD_HHMMSS.json`

### 8.3 Restore Data
- Root users can restore from backup file
- Upload JSON backup file
- Preview changes before applying
- Shows: Companies to add, Records to add/update

### 8.4 Preview Restore
- Shows what will be changed
- Displays statistics:
  - Companies count
  - Attendance records count
  - Mandays records count
  - Users count
- User can review before applying

### 8.5 Apply Restore
- Applies the restore operation
- Creates new companies
- Creates/updates attendance records
- Creates/updates mandays records
- Creates new users
- Skips existing records (no duplicates)
- Creates restore log with statistics
- Success message with details

---

## 9. Audit & Logging

### 9.1 Upload Logs
- Tracks all CSV/Excel uploads
- Records: User, Filename, Timestamp, Success/Updated/Error counts, Error messages
- Accessible by Root and Admin users
- Helps troubleshoot upload issues

### 9.2 Mandays Upload Logs
- Tracks all mandays CSV/Excel uploads
- Records: User, Filename, Timestamp, Success/Updated/Error counts, Error messages
- Accessible by Root and Admin users

### 9.3 Backup Logs
- Tracks all backup and restore operations
- Records: User, Operation Type, Filename, Timestamp, Statistics, Success/Failure
- Accessible by Root users only

### 9.4 Access Request Audit Log
- Tracks all access control actions
- Records:
  - Request created
  - Request approved
  - Request rejected
  - Request cancelled
  - Assignment created
  - Assignment removed
  - Assignment expired
- Includes: Actor, Target User, Employee Number, Timestamp, Details (JSON)
- Helps with compliance and security audits

### 9.5 System Logs
- All major actions logged to file
- Log levels: DEBUG, INFO, WARNING, ERROR
- Includes: User actions, Authentication events, Data operations, Errors
- Log file: `logs/attendance_system.log`

---

## 10. Data Import/Export

### 10.1 CSV Import Features
- Automatic company detection and creation
- Handles multiple date formats
- Handles multiple time formats
- Validates required fields
- Skips invalid rows with error messages
- Updates existing records
- Creates new records
- Progress tracking for large files

### 10.2 Excel Export Features
- Exports to XLSX format
- Formatted headers with styling
- Auto-adjusted column widths
- Includes all data fields
- Applies current filters
- Timestamp in filename

### 10.3 CSV Template Download
- Provides sample template
- Shows required columns
- Includes example data
- Helps users format uploads correctly

---

## 11. Multi-Tenant Architecture

### 11.1 Company Isolation
- All data belongs to a company
- Users assigned to companies
- Data queries filtered by company
- Root users can access all companies
- Admin users restricted to their company
- User1 restricted to their company and assigned employees

### 11.2 Company Management
- Companies created automatically during uploads
- Company name extracted from data
- Unique company names enforced
- 104 companies currently in system

---

## 12. Data Validation & Integrity

### 12.1 Attendance Record Validation
- Unique constraint: (Employee Number, Date)
- Required fields: EP NO, EP Name, Company, Date, Shift, Status
- Optional fields: IN/OUT times, Overtime, Overstay
- Status must be valid: P, A, PH, WO, -0.5, -1
- Date format validation
- Time format validation

### 12.2 Mandays Record Validation
- Unique constraint: (Employee Number, Punch Date)
- Required fields: EP NO, Company, Punch Date, Mandays, OT
- OT converted from time to decimal format
- Date format validation
- Decimal format validation

### 12.3 User Validation
- Unique username required
- Admin and User1 must have company assigned
- User1 date range validation (from < to)
- Password strength requirements
- Role validation

### 12.4 Access Request Validation
- Date range requests must have both dates
- Date range validation (from < to)
- Employee must exist in company
- No duplicate pending requests
- Justification required

---

## 13. User Interface Features

### 13.1 Responsive Design
- Mobile-first approach
- Card layout for mobile devices
- Table layout for desktop devices
- Touch-friendly buttons and controls
- Optimized for all screen sizes

### 13.2 Navigation
- Fixed header with navigation menu
- Mobile bottom navigation dock
- Role-based menu items
- Quick access to common features
- User profile display

### 13.3 Filtering & Search
- Advanced filter options
- Real-time search
- Filter persistence across pages
- Clear filter option
- Filter indicators

### 13.4 Pagination
- 50 records per page
- Page navigation controls
- Total records count
- Jump to page option
- Maintains filters across pages

### 13.5 Messages & Notifications
- Success messages (green)
- Error messages (red)
- Warning messages (yellow)
- Info messages (blue)
- Auto-dismiss after 5 seconds

### 13.6 Forms
- Inline validation
- Error highlighting
- Help text for fields
- Required field indicators
- Date pickers for date fields
- Dropdown selects for choices

---

## 14. Performance Features

### 14.1 Database Optimization
- Indexed columns for fast queries
- Composite indexes for multi-column filters
- Query optimization with select_related
- Batch processing for large datasets
- Iterator for memory-efficient processing

### 14.2 Caching
- Upload progress cached
- Session data cached
- Reduces database queries

### 14.3 Pagination
- Limits records per page
- Reduces memory usage
- Faster page loads

---

## 15. Security Features

### 15.1 Authentication
- Password hashing (Django default)
- Session-based authentication
- CSRF protection
- Login required for all pages (except login)

### 15.2 Authorization
- Role-based access control
- Company-level data isolation
- Employee-level access control (User1)
- Permission checks on every action

### 15.3 Data Protection
- SQL injection prevention (Django ORM)
- XSS protection (Django templates)
- CSRF tokens on all forms
- Secure session management

### 15.4 Audit Trail
- All actions logged
- User actions tracked
- Access control changes logged
- Helps with compliance and forensics

---

## 16. Error Handling

### 16.1 User-Friendly Error Messages
- Clear error descriptions
- Actionable error messages
- No technical jargon
- Helpful suggestions

### 16.2 Error Logging
- All errors logged to file
- Stack traces captured
- User context included
- Helps with debugging

### 16.3 Graceful Degradation
- System continues working on errors
- Partial data displayed when possible
- Error recovery mechanisms
- User notified of issues

---

## 17. Data Statistics

### Current System Data:
- **Total Tables:** 13
- **Total Records:** ~133,438
- **Attendance Records:** 96,315
- **Mandays Records:** 37,086
- **Companies:** 104
- **Users:** 3
- **Upload Logs:** 21 (Attendance) + 4 (Mandays)
- **Access Requests:** 1
- **Employee Assignments:** 1
- **Audit Logs:** 6
- **Backup Logs:** 1

---

## 18. System Requirements

### 18.1 Server Requirements
- Python 3.11+
- Django 4.2.7
- SQLite 3 (or PostgreSQL for production)
- 2GB RAM minimum
- 10GB disk space

### 18.2 Browser Requirements
- Modern browsers (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- Cookies enabled
- Responsive design support

---

## 19. Future Enhancements (Not Currently Implemented)

### Potential Features:
- Email notifications for access requests
- Advanced reporting and analytics
- Data archiving for old records
- Mobile app
- API for third-party integrations
- Real-time attendance tracking
- Biometric integration
- Shift scheduling
- Leave management
- Payroll integration

---

## Summary

This Attendance Management System is a comprehensive, multi-tenant web application designed to manage employee attendance and mandays data with sophisticated role-based access control. The system supports three user roles (Root, Admin, User1) with different permission levels, provides advanced filtering and export capabilities, includes a complete access request workflow for supervisors, and maintains comprehensive audit trails for compliance and security.

The system is production-ready, currently managing 96,315 attendance records and 37,086 mandays records across 104 companies, with robust data validation, security features, and a responsive user interface optimized for both mobile and desktop devices.
