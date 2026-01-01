# User Roles and Functionality

## Overview
The Attendance Management System has three distinct user roles, each with specific permissions and access levels.

---

## 1. Root User

### Description
The Root user is the super administrator with complete system access across all companies and data.

### Permissions & Functionality

#### Full System Access
- ✅ Access data from **ALL companies** without restrictions
- ✅ View, edit, and delete attendance records across all companies
- ✅ No date range restrictions

#### User Management
- ✅ Create, edit, and delete all user accounts (Root, Admin, User1)
- ✅ Assign companies to Admin and User1 users
- ✅ Set date-based access control for User1
- ✅ Manage user permissions

#### Data Management
- ✅ Upload attendance data for any company
- ✅ Bulk import via CSV/Excel files
- ✅ Export data for any company
- ✅ Backup and restore operations
- ✅ Full backup (all companies)
- ✅ Incremental backup

#### Access Request Management
- ✅ View all access requests from User1
- ✅ Approve or reject access requests
- ✅ Manage employee assignments for User1

#### System Administration
- ✅ Configure system settings
- ✅ View audit logs
- ✅ Monitor upload history
- ✅ Manage upload permissions

---

## 2. Admin User

### Description
Admin users manage attendance data for their assigned company only. Each Admin is tied to a specific company.

### Permissions & Functionality

#### Company-Specific Access
- ✅ Access data **ONLY for their assigned company**
- ✅ View, edit, and delete attendance records for their company
- ✅ No date range restrictions
- ⛔ Cannot access other companies' data

#### Data Management
- ✅ Upload attendance data for their company only
- ✅ Bulk import via CSV/Excel files (company validation enforced)
- ✅ Export data for their company
- ✅ Backup operations for their company data

#### User1 Management
- ✅ Create and manage User1 accounts for their company
- ✅ Assign employees to User1 supervisors
- ✅ Set date-based access control for User1
- ✅ View and manage access requests from User1

#### Remark Management
- ✅ Create and manage remark reasons/categories
- ✅ View remarks added by User1
- ✅ Respond to User1 remarks
- ✅ Update remark status (pending/reviewed/resolved)

#### Restrictions
- ⛔ Cannot create Root or Admin users
- ⛔ Cannot access other companies' data
- ⛔ Cannot modify system-wide settings
- ⛔ Upload validation enforces company match

---

## 3. User1 (Supervisor)

### Description
User1 is a supervisor role with limited, date-based access to specific employees' attendance data.

### Permissions & Functionality

#### Limited Data Access
- ✅ View attendance data **ONLY for assigned employees**
- ✅ Access restricted by date range (assigned_date_from to assigned_date_to)
- ✅ Can request access to additional employees
- ⛔ Cannot view unassigned employees
- ⛔ Cannot edit or delete attendance records

#### Employee Assignment
- Employees are assigned to User1 by Admin or Root
- Each assignment has:
  - Employee EP Number
  - Access date range (from/to) or permanent access
  - Assignment source (admin assigned or access request)
  - Active/inactive status

#### Access Request System
- ✅ Request access to specific employees
- ✅ Specify date range or permanent access
- ✅ Provide justification for access request
- ✅ View status of requests (pending/approved/rejected)
- ✅ Cancel pending requests
- ⛔ Cannot approve own requests

#### Remark System
- ✅ Add remarks/comments to attendance records
- ✅ Select from predefined remark reasons
- ✅ View Admin responses to remarks
- ✅ Track remark status

#### Restrictions
- ⛔ Cannot upload data
- ⛔ Cannot edit attendance records
- ⛔ Cannot delete records
- ⛔ Cannot create users
- ⛔ Cannot access data outside assigned date range
- ⛔ Cannot view other supervisors' assigned employees

---

## User Role Comparison Table

| Feature | Root | Admin | User1 |
|---------|------|-------|-------|
| **Data Access** |
| All Companies | ✅ | ⛔ | ⛔ |
| Single Company | ✅ | ✅ | ⛔ |
| Assigned Employees Only | ✅ | ✅ | ✅ |
| Date Range Restriction | ⛔ | ⛔ | ✅ |
| **Data Operations** |
| View Records | ✅ | ✅ | ✅ |
| Edit Records | ✅ | ✅ | ⛔ |
| Delete Records | ✅ | ✅ | ⛔ |
| Upload Data | ✅ | ✅ | ⛔ |
| Export Data | ✅ | ✅ | ⛔ |
| **User Management** |
| Create Root Users | ✅ | ⛔ | ⛔ |
| Create Admin Users | ✅ | ⛔ | ⛔ |
| Create User1 | ✅ | ✅ | ⛔ |
| Assign Employees to User1 | ✅ | ✅ | ⛔ |
| **Access Requests** |
| Submit Requests | ⛔ | ⛔ | ✅ |
| Approve/Reject Requests | ✅ | ✅ | ⛔ |
| **Remarks** |
| Add Remarks | ✅ | ✅ | ✅ |
| Respond to Remarks | ✅ | ✅ | ⛔ |
| Manage Remark Reasons | ✅ | ✅ | ⛔ |
| **System Admin** |
| Backup/Restore | ✅ | ✅ (own company) | ⛔ |
| View Audit Logs | ✅ | ✅ (own company) | ⛔ |
| System Settings | ✅ | ⛔ | ⛔ |

---

## Access Control Examples

### Example 1: Root User
- **User**: root_user
- **Company**: None (all companies)
- **Access**: All attendance records from all companies, all dates

### Example 2: Admin User
- **User**: admin_reliance
- **Company**: Reliance Industries
- **Access**: All attendance records for Reliance Industries only, all dates
- **Restriction**: Cannot view/edit data from other companies

### Example 3: User1 (Supervisor)
- **User**: supervisor_john
- **Company**: Reliance Industries
- **Assigned Employees**: EP001, EP002, EP003
- **Date Range**: 2025-01-01 to 2025-12-31
- **Access**: Can only view attendance for EP001, EP002, EP003 between Jan 1 - Dec 31, 2025
- **Restriction**: Cannot view other employees or dates outside range

---

## Date-Based Access Control (User1)

### Permanent Access
- No date restrictions
- User1 can view assigned employees' data for all dates
- Set by leaving `access_from` and `access_to` blank

### Date Range Access
- User1 can only view data within specified date range
- Example: `access_from: 2025-01-01`, `access_to: 2025-12-31`
- Attempting to view data outside range shows "Access Denied"

### User-Level Date Range
- Admin can set overall date range for User1 account
- `assigned_date_from` and `assigned_date_to` on User model
- Applies to all employee assignments for that User1

---

## Access Request Workflow

### Step 1: User1 Submits Request
- Selects employee EP number
- Chooses access type (date range or permanent)
- Provides justification
- Request status: **Pending**

### Step 2: Admin/Root Reviews
- Views pending requests
- Reviews justification
- Can approve or reject

### Step 3: Approval
- If approved: Employee assignment created automatically
- User1 gains access immediately
- Request status: **Approved**

### Step 4: Rejection
- If rejected: Admin provides rejection reason
- User1 notified
- Request status: **Rejected**

---

## Remark System Workflow

### Step 1: User1 Adds Remark
- Views attendance record
- Clicks "Add Remark"
- Selects remark reason (from predefined list)
- Adds comment/details
- Remark status: **Pending**

### Step 2: Admin Reviews
- Views remarks for their company
- Reads User1's comment
- Adds response
- Updates status to **Reviewed** or **Resolved**

### Step 3: User1 Views Response
- Sees Admin's response
- Can add follow-up remarks if needed

---

## Security & Validation

### Company Access Validation
- Admin users: Upload validation enforces company match
- User1: Query filters automatically apply company + employee + date restrictions
- Root: No restrictions

### Date Range Validation
- User1 date ranges validated on:
  - Login
  - Every data query
  - Access request submission
- Invalid date ranges rejected

### Upload Validation
- Admin uploads: Company name in file must match assigned company
- Root uploads: No company restrictions
- User1: Cannot upload

---

## Best Practices

### For Root Users
- Create Admin users for each company
- Assign appropriate permissions
- Monitor audit logs regularly
- Review and approve access requests promptly

### For Admin Users
- Create User1 accounts for supervisors
- Assign employees based on reporting structure
- Set appropriate date ranges
- Review and respond to remarks regularly
- Manage remark reasons/categories

### For User1 Users
- Request access only for employees you supervise
- Provide clear justification for access requests
- Use remarks to communicate issues to Admin
- Check remark responses regularly

---

## Common Scenarios

### Scenario 1: New Supervisor Onboarding
1. Admin creates User1 account
2. Admin assigns employees to User1
3. Admin sets date range (e.g., current year)
4. User1 logs in and can view assigned employees

### Scenario 2: Temporary Access Request
1. User1 needs access to employee for specific period
2. User1 submits access request with date range
3. Admin reviews and approves
4. User1 gains access for specified period
5. Access automatically expires after end date

### Scenario 3: Attendance Issue Reporting
1. User1 notices attendance discrepancy
2. User1 adds remark with details
3. Admin receives notification
4. Admin investigates and responds
5. Admin marks as resolved

---

## Audit & Compliance

### Audit Logs Track
- User login/logout
- Data access (who viewed what)
- Data modifications (create/update/delete)
- Access request submissions and approvals
- Employee assignment changes
- Remark additions and responses

### Compliance Features
- Date-based access control
- Company data isolation
- Access request justification
- Audit trail for all actions
- Role-based permissions

---

## Support & Troubleshooting

### Common Issues

**Issue**: Admin cannot upload data
- **Solution**: Ensure company name in file matches assigned company

**Issue**: User1 cannot see employee data
- **Solution**: Check if employee is assigned and date is within range

**Issue**: Access request rejected
- **Solution**: Review rejection reason and resubmit with better justification

**Issue**: Cannot view old data
- **Solution**: Check date range restrictions for User1 accounts

---

## System URLs

- **Login**: `/login/`
- **Attendance List**: `/attendance/`
- **Upload Data**: `/upload/` (Root/Admin only)
- **Excel Upload**: `/excel/upload/` (Root/Admin only)
- **Access Requests**: `/access-requests/` (User1)
- **Manage Assignments**: `/manage-assignments/` (Root/Admin)
- **Remarks**: `/remarks/` (All users)
- **Backup**: `/backup/` (Root/Admin)

---

*Last Updated: December 29, 2025*
