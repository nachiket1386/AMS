# Backend Architecture Design Document

## Overview

The Attendance Management System is a Django-based web application that provides comprehensive employee attendance tracking with multi-tenant support. The backend architecture follows Django's MVT (Model-View-Template) pattern with additional layers for business logic, data validation, and access control.

### Key Features

- **Multi-Tenant Architecture**: Complete data isolation between companies
- **Role-Based Access Control**: Three-tier permission system (Root, Admin, User1)
- **CSV Import/Export**: Bulk data operations with validation
- **Audit Logging**: Complete tracking of data operations
- **RESTful URL Design**: Clean, intuitive endpoint structure
- **Security First**: Input validation, CSRF protection, permission checks

### Technology Stack

- **Framework**: Django 4.2.7
- **Database**: SQLite (development), PostgreSQL (production ready)
- **ORM**: Django ORM
- **Authentication**: Django Auth with custom User model
- **File Processing**: Python CSV module, openpyxl for Excel
- **Logging**: Python logging module with file and console handlers

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│                    (Browser / HTTP Client)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Django Middleware                        │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │ Security │ Session  │   CSRF   │   Auth   │ Messages │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                       URL Router                             │
│              (attendance_system/urls.py)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                       View Layer                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Decorators: @login_required, @role_required,        │  │
│  │              @company_access_required                 │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Views: login, dashboard, attendance_list,           │  │
│  │         upload_csv, export, user_management          │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬───────────────────────────┬────────────────────┘
             │                           │
             ▼                           ▼
┌────────────────────────┐   ┌──────────────────────────────┐
│   Business Logic       │   │      Form Validation         │
│  ┌──────────────────┐  │   │  ┌────────────────────────┐ │
│  │  CSV Processor   │  │   │  │  LoginForm             │ │
│  │  - validate_csv  │  │   │  │  AttendanceRecordForm  │ │
│  │  - process_row   │  │   │  │  UserForm              │ │
│  │  - validate_date │  │   │  └────────────────────────┘ │
│  │  - validate_time │  │   └──────────────────────────────┘
│  └──────────────────┘  │
└────────────┬───────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                       Model Layer (ORM)                      │
│  ┌──────────┬──────────────────┬──────────┬─────────────┐  │
│  │ Company  │ User (Custom)    │ Attendance│ UploadLog  │  │
│  │          │                  │  Record   │            │  │
│  └──────────┴──────────────────┴──────────┴─────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer                            │
│              (SQLite / PostgreSQL)                           │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow

1. **Client Request** → HTTP request to Django server
2. **Middleware Processing** → Security, session, CSRF, authentication
3. **URL Routing** → Match URL pattern to view function
4. **Decorator Execution** → Check authentication and permissions
5. **View Processing** → Business logic, form validation, data queries
6. **Model Operations** → ORM queries to database
7. **Response Generation** → Render template or return data
8. **Middleware Response** → Add headers, process cookies
9. **Client Response** → HTML page or file download

## Components and Interfaces

### 1. Data Models

#### Company Model

```python
class Company(models.Model):
    """Represents a tenant organization"""
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Relationships:
    # - users (reverse FK from User)
    # - attendance_records (reverse FK from AttendanceRecord)
```

**Purpose**: Multi-tenant data isolation
**Key Features**:
- Unique company names
- Automatic timestamp tracking
- Cascade relationships for data integrity

#### User Model (Custom)

```python
class User(AbstractUser):
    """Custom user with role-based access"""
    ROLE_CHOICES = [
        ('root', 'Root'),
        ('admin', 'Admin'),
        ('user1', 'User1'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user1')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, 
                                null=True, blank=True)
    
    # Inherited from AbstractUser:
    # - username, password, email, first_name, last_name
    # - is_active, is_staff, is_superuser
    # - date_joined, last_login
```

**Purpose**: Authentication and authorization
**Key Features**:
- Extends Django's AbstractUser
- Role-based permissions
- Company association for data isolation
- Built-in password hashing and session management

**Validation Rules**:
- Admin and User1 must have company assigned
- Username must be unique
- Password minimum 6 characters

#### AttendanceRecord Model

```python
class AttendanceRecord(models.Model):
    """Employee attendance data"""
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('PH', 'Public Holiday'),
        ('-0.5', 'Half Day'),
        ('-1', 'Full Day Leave'),
    ]
    
    # Required fields
    ep_no = models.CharField(max_length=50)
    ep_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    shift = models.CharField(max_length=50)
    overstay = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    # Optional time fields
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)
    in_time_2 = models.TimeField(null=True, blank=True)
    out_time_2 = models.TimeField(null=True, blank=True)
    in_time_3 = models.TimeField(null=True, blank=True)
    out_time_3 = models.TimeField(null=True, blank=True)
    overtime = models.TimeField(null=True, blank=True)
    overtime_to_mandays = models.TimeField(null=True, blank=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Constraints
    unique_together = ['ep_no', 'date']
    
    # Indexes
    indexes = [
        models.Index(fields=['ep_no', 'date']),
        models.Index(fields=['company', 'date']),
        models.Index(fields=['date']),
    ]
```

**Purpose**: Store employee attendance records
**Key Features**:
- Unique constraint on employee + date
- Multiple time punch support (3 in/out pairs)
- Overtime tracking
- Automatic timestamps
- Optimized indexes for common queries

#### UploadLog Model

```python
class UploadLog(models.Model):
    """Audit trail for CSV uploads"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    success_count = models.IntegerField(default=0)
    updated_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    error_messages = models.TextField(blank=True)
    
    # Indexes
    indexes = [
        models.Index(fields=['user', 'uploaded_at']),
        models.Index(fields=['uploaded_at']),
    ]
```

**Purpose**: Audit logging for data imports
**Key Features**:
- Track who uploaded what and when
- Success/error statistics
- Detailed error messages for troubleshooting
- Indexed for fast querying

### 2. View Layer

#### Authentication Views

**login_view(request)**
- **Purpose**: Handle user authentication
- **Method**: GET (show form), POST (process login)
- **Permissions**: Public
- **Logic**:
  1. Check if user already authenticated → redirect to dashboard
  2. On POST: validate credentials
  3. If valid: create session, log event, redirect
  4. If invalid: show error, log failed attempt
- **Returns**: Login template or redirect

**logout_view(request)**
- **Purpose**: End user session
- **Method**: GET/POST
- **Permissions**: Any authenticated user
- **Logic**:
  1. Log username before logout
  2. Clear session
  3. Show success message
  4. Redirect to login
- **Returns**: Redirect to login page

#### Dashboard View

**dashboard_view(request)**
- **Purpose**: Display system overview and statistics
- **Method**: GET
- **Permissions**: @login_required
- **Logic**:
  1. Calculate statistics based on user role
  2. Root: all companies, all records
  3. Admin/User1: own company only
  4. Fetch recent upload logs
  5. Render dashboard template
- **Returns**: Dashboard template with context

#### Attendance Management Views

**attendance_list_view(request)**
- **Purpose**: List attendance records with filtering
- **Method**: GET
- **Permissions**: @login_required, @company_access_required
- **Query Parameters**:
  - date_from: Start date filter
  - date_to: End date filter
  - company: Company filter (Root only)
  - ep_no: Employee number search
  - status: Status filter
  - page: Pagination page number
- **Logic**:
  1. Build base queryset by role
  2. Apply filters from query parameters
  3. Paginate results (50 per page)
  4. Add shift_code attribute to records
  5. Fetch companies for filter dropdown (Root only)
- **Returns**: List template with paginated records

**attendance_export_view(request)**
- **Purpose**: Export attendance data to XLSX
- **Method**: GET
- **Permissions**: @login_required, @company_access_required
- **Query Parameters**: Same as attendance_list_view
- **Logic**:
  1. Apply same filters as list view
  2. Create Excel workbook with openpyxl
  3. Style headers (blue background, white text, bold)
  4. Write data rows with formatted dates/times
  5. Auto-adjust column widths
  6. Generate filename with timestamp
- **Returns**: XLSX file download

**attendance_edit_view(request, record_id)**
- **Purpose**: Edit existing attendance record
- **Method**: GET (show form), POST (save changes)
- **Permissions**: @role_required(['root', 'admin'])
- **Logic**:
  1. Fetch record or 404
  2. Check company access
  3. On GET: render form with current data
  4. On POST: validate and save changes
  5. Show success message
- **Returns**: Edit form or redirect to list

**attendance_delete_view(request, record_id)**
- **Purpose**: Delete attendance record
- **Method**: POST
- **Permissions**: @role_required(['root', 'admin'])
- **Logic**:
  1. Fetch record or 404
  2. Check company access
  3. Delete record
  4. Show success message
- **Returns**: Redirect to list

#### CSV Upload Views

**upload_csv_view(request)**
- **Purpose**: Handle CSV file uploads
- **Method**: GET (show form), POST (process file)
- **Permissions**: @role_required(['root', 'admin'])
- **Logic**:
  1. On GET: show upload form with recent logs
  2. On POST:
     - Validate file extension (.csv)
     - Create CSVProcessor instance
     - Process file (validate and import)
     - Create UploadLog entry
     - Log results
     - Display success/error messages
  3. Fetch recent logs filtered by role
- **Returns**: Upload template or redirect

**download_csv_template(request)**
- **Purpose**: Provide CSV template file
- **Method**: GET
- **Permissions**: @role_required(['root', 'admin'])
- **Logic**:
  1. Create CSV response
  2. Write header row with all columns
  3. Log download event
- **Returns**: CSV file download

**upload_logs_view(request)**
- **Purpose**: View upload history
- **Method**: GET
- **Permissions**: @role_required(['root', 'admin'])
- **Logic**:
  1. Fetch logs filtered by role
  2. Paginate results (20 per page)
  3. Render logs template
- **Returns**: Logs template with pagination

#### User Management Views

**user_list_view(request)**
- **Purpose**: List system users
- **Method**: GET
- **Permissions**: @role_required(['root', 'admin'])
- **Logic**:
  1. Root: fetch all users
  2. Admin: fetch User1 in own company
  3. Render user list
- **Returns**: User list template

**user_create_view(request)**
- **Purpose**: Create new user
- **Method**: GET (show form), POST (create user)
- **Permissions**: @role_required(['root', 'admin'])
- **Logic**:
  1. On GET: render empty form
  2. On POST:
     - Validate form data
     - Admin: auto-assign company and User1 role
     - Hash password
     - Save user
     - Show success message
- **Returns**: User form or redirect to list

**user_edit_view(request, user_id)**
- **Purpose**: Edit existing user
- **Method**: GET (show form), POST (save changes)
- **Permissions**: @role_required(['root', 'admin'])
- **Logic**:
  1. Fetch user or 404
  2. Check permissions (Admin can only edit User1 in own company)
  3. On GET: render form with current data
  4. On POST: validate and save
- **Returns**: User form or redirect to list

**user_delete_view(request, user_id)**
- **Purpose**: Delete user
- **Method**: GET (confirm), POST (delete)
- **Permissions**: @role_required(['root'])
- **Logic**:
  1. Fetch user or 404
  2. Prevent self-deletion
  3. Prevent deleting Root users
  4. On POST: delete user and log event
- **Returns**: Confirmation template or redirect

#### Export Views

**export_csv_view(request)**
- **Purpose**: Export attendance data to CSV
- **Method**: GET
- **Permissions**: @login_required
- **Query Parameters**: Same as attendance_list_view
- **Logic**:
  1. Apply same filters as list view
  2. Create CSV response
  3. Write header row
  4. Write data rows with formatted dates/times
  5. Generate filename with timestamp
- **Returns**: CSV file download

### 3. Business Logic Components

#### CSVProcessor Class

**Purpose**: Validate and process CSV attendance files

**Attributes**:
- `REQUIRED_FIELDS`: List of mandatory CSV columns
- `OPTIONAL_FIELDS`: List of optional CSV columns
- `VALID_STATUS`: List of allowed status values
- `errors`: List to collect validation errors
- `success_count`: Counter for created records
- `updated_count`: Counter for updated records
- `error_count`: Counter for failed rows

**Methods**:

**validate_csv(file) → dict**
- Validates CSV structure and headers
- Checks for required columns
- Returns: `{'valid': bool, 'errors': list}`

**validate_date(date_str) → date | None**
- Accepts YYYY-MM-DD or DD-MM-YYYY formats
- Rejects future dates
- Returns: date object or None

**validate_time(time_str) → time | None**
- Accepts HH:MM format
- Handles (N) suffixes like "09:00 (1)"
- Returns: time object or None

**validate_status(status) → bool**
- Checks if status is in VALID_STATUS list
- Returns: boolean

**process_row(row, row_number, user) → tuple**
- Validates all fields in a CSV row
- Checks company access for Admin users
- Creates/gets Company object
- Returns: `(success: bool, error_msg: str, data: dict)`

**create_or_update_record(data) → tuple**
- Uses update_or_create for upsert operation
- Unique key: ep_no + date
- Returns: `(created: bool, updated: bool)`

**process_csv(file, user) → dict**
- Main entry point for CSV processing
- Validates structure
- Processes all rows
- Collects statistics
- Returns: `{'success': bool, 'errors': list, 'success_count': int, 'updated_count': int, 'error_count': int}`

### 4. Security Components

#### Decorators

**@role_required(allowed_roles)**
- **Purpose**: Restrict access by user role
- **Parameters**: List of allowed roles
- **Logic**:
  1. Check if user authenticated (via @login_required)
  2. Check if user.role in allowed_roles
  3. If yes: execute view
  4. If no: log attempt, show error, return 403
- **Usage**: `@role_required(['root', 'admin'])`

**@company_access_required**
- **Purpose**: Ensure user has company assignment
- **Logic**:
  1. Root users: always pass
  2. Admin/User1: check company is assigned
  3. If no company: redirect to dashboard with error
- **Usage**: Applied to views that query company data

**Helper Functions**:

**check_record_company_access(user, record) → bool**
- Validates user can access specific record's company
- Root: always True
- Others: True if record.company == user.company

**can_edit_record(user) → bool**
- Returns True if user role in ['root', 'admin']

**can_delete_record(user) → bool**
- Returns True if user role in ['root', 'admin']

**can_upload_csv(user) → bool**
- Returns True if user role in ['root', 'admin']

**can_manage_users(user) → bool**
- Returns True if user role in ['root', 'admin']

### 5. Form Validation

#### LoginForm

```python
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
```

**Purpose**: User authentication
**Validation**: Handled by Django's AuthenticationForm

#### AttendanceRecordForm

```python
class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = [all attendance fields]
```

**Purpose**: Create/edit attendance records
**Custom Validation**:
- `clean_date()`: Reject future dates
- `clean_ep_no()`: Strip whitespace, reject empty
- `clean_ep_name()`: Strip whitespace, reject empty

#### UserForm

```python
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'role', 'company', 'is_active']
```

**Purpose**: Create/edit users
**Custom Validation**:
- `clean_username()`: Check uniqueness, convert to lowercase
- `clean_password()`: Minimum 6 characters
- `clean()`: Validate Admin/User1 have company
**Dynamic Behavior**:
- Admin users: restrict to User1 role, hide company field

## Data Models

### Entity Relationship Diagram

```
┌─────────────────┐
│    Company      │
│─────────────────│
│ id (PK)         │
│ name (UNIQUE)   │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         │
    ┌────┴────────────────────────────┐
    │                                 │
    │                                 │
┌───▼──────────────┐         ┌────────▼──────────┐
│      User        │         │ AttendanceRecord  │
│──────────────────│         │───────────────────│
│ id (PK)          │         │ id (PK)           │
│ username (UNIQUE)│         │ ep_no             │
│ password         │         │ ep_name           │
│ role             │         │ company_id (FK)   │
│ company_id (FK)  │         │ date              │
│ is_active        │         │ shift             │
│ date_joined      │         │ status            │
│ last_login       │         │ in_time           │
└────────┬─────────┘         │ out_time          │
         │                   │ ... (more times)  │
         │ 1:N               │ created_at        │
         │                   │ updated_at        │
    ┌────▼────────┐          │ UNIQUE(ep_no,date)│
    │  UploadLog  │          └───────────────────┘
    │─────────────│
    │ id (PK)     │
    │ user_id (FK)│
    │ uploaded_at │
    │ filename    │
    │ success_cnt │
    │ updated_cnt │
    │ error_count │
    │ error_msgs  │
    └─────────────┘
```

### Database Indexes

**AttendanceRecord**:
- `idx_ep_no_date`: Composite index on (ep_no, date) - for unique lookups
- `idx_company_date`: Composite index on (company_id, date) - for filtered queries
- `idx_date`: Single index on date - for date range queries

**UploadLog**:
- `idx_user_uploaded_at`: Composite index on (user_id, uploaded_at) - for user history
- `idx_uploaded_at`: Single index on uploaded_at - for recent logs

### Data Integrity Rules

1. **Referential Integrity**:
   - AttendanceRecord.company → Company (CASCADE delete)
   - User.company → Company (SET NULL on delete)
   - UploadLog.user → User (CASCADE delete)

2. **Uniqueness Constraints**:
   - Company.name must be unique
   - User.username must be unique
   - AttendanceRecord (ep_no, date) must be unique

3. **Validation Constraints**:
   - User.role must be in ['root', 'admin', 'user1']
   - AttendanceRecord.status must be in ['P', 'A', 'PH', 'L', '-0.5', '-1']
   - AttendanceRecord.date cannot be in future
   - Admin/User1 must have company assigned

## 
## C
orrectness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Company Creation Assigns Metadata
*For any* company creation, the system should automatically assign a unique identifier and timestamp.
**Validates: Requirements 1.2**

### Property 2: Non-Root Users Require Company
*For any* user with role Admin or User1, attempting to save without an assigned company should fail validation.
**Validates: Requirements 1.4, 3.5**

### Property 3: Company-Based Record Filtering
*For any* authenticated non-root user querying attendance records, the results should only include records from their assigned company.
**Validates: Requirements 1.5**

### Property 4: Root User Universal Access
*For any* data query by a root user, the system should return records from all companies without filtering.
**Validates: Requirements 2.2**

### Property 5: Admin Company Isolation
*For any* admin user querying data, the system should restrict results to only their assigned company's records.
**Validates: Requirements 2.3**

### Property 6: User1 Read-Only Access
*For any* User1 attempting write operations (create, update, delete), the system should deny access and return 403.
**Validates: Requirements 2.4**

### Property 7: Unauthorized Access Returns 403
*For any* user attempting to access a resource without proper role permissions, the system should return HTTP 403 and log the attempt.
**Validates: Requirements 2.6**

### Property 8: Credential Authentication
*For any* login attempt with valid credentials, the system should authenticate successfully; for invalid credentials, authentication should fail.
**Validates: Requirements 3.2**

### Property 9: Successful Login Session Creation
*For any* successful authentication, the system should create a session and redirect to the dashboard.
**Validates: Requirements 3.3**

### Property 10: Failed Login Error Display
*For any* failed authentication attempt, the system should display an error message and log the failed attempt.
**Validates: Requirements 3.4**

### Property 11: Root User Creation Permissions
*For any* user creation by a root user, the system should allow assignment of any role and any company.
**Validates: Requirements 3.6**

### Property 12: Admin User Creation Restrictions
*For any* user creation by an admin user, the system should restrict the role to User1 and company to the admin's company.
**Validates: Requirements 3.7**

### Property 13: Attendance Record Uniqueness
*For any* attendance record, attempting to create a duplicate with the same employee number and date should either update the existing record or fail with a uniqueness error.
**Validates: Requirements 4.2**

### Property 14: Attendance Filtering Behavior
*For any* combination of filters (date range, company, employee number, status), the system should return only records matching all applied filters.
**Validates: Requirements 4.4**

### Property 15: Cross-Company Edit Prevention
*For any* admin user attempting to edit a record from a different company, the system should deny access.
**Validates: Requirements 4.5**

### Property 16: Automatic Timestamp Updates
*For any* attendance record update, the system should automatically update the updated_at timestamp to the current time.
**Validates: Requirements 4.6**

### Property 17: CSV File Extension Validation
*For any* file upload, if the extension is not .csv, the system should reject the upload with a validation error.
**Validates: Requirements 5.1**

### Property 18: CSV Required Columns Validation
*For any* CSV file missing required columns (EP NO, EP NAME, COMPANY NAME, DATE, SHIFT, STATUS), the system should reject the file with an error listing missing columns.
**Validates: Requirements 5.2**

### Property 19: CSV Date Format Validation
*For any* CSV row with a date field, the system should accept YYYY-MM-DD or DD-MM-YYYY formats and reject other formats.
**Validates: Requirements 5.3**

### Property 20: Future Date Rejection
*For any* attendance record or CSV row with a future date, the system should reject it with a validation error.
**Validates: Requirements 5.4, 10.5**

### Property 21: Time Format Validation
*For any* CSV time field, the system should accept HH:MM format with optional (N) suffix and reject invalid formats.
**Validates: Requirements 5.5**

### Property 22: Status Value Validation
*For any* attendance record status, the system should accept only values in [P, A, PH, L, -0.5, -1] and reject others.
**Validates: Requirements 5.6**

### Property 23: Admin CSV Company Restriction
*For any* CSV upload by an admin user containing records from a different company, the system should reject those rows with an error.
**Validates: Requirements 5.7**

### Property 24: CSV Upsert Behavior
*For any* CSV row with an employee number and date matching an existing record, the system should update the existing record rather than creating a duplicate.
**Validates: Requirements 5.8**

### Property 25: Upload Log Creation
*For any* CSV upload operation, the system should create an UploadLog entry with accurate success count, update count, and error count.
**Validates: Requirements 5.9, 7.1**

### Property 26: CSV Error Collection
*For any* CSV file with multiple invalid rows, the system should process all rows and collect all validation errors rather than stopping at the first error.
**Validates: Requirements 5.10, 12.1**

### Property 27: Export Filter Consistency
*For any* export operation with applied filters, the exported data should match exactly what appears in the filtered list view.
**Validates: Requirements 6.2**

### Property 28: Root Export Completeness
*For any* export by a root user, the exported data should include records from all companies.
**Validates: Requirements 6.3**

### Property 29: Non-Root Export Isolation
*For any* export by an admin or User1, the exported data should include only records from their assigned company.
**Validates: Requirements 6.4**

### Property 30: XLSX Column Width Adjustment
*For any* XLSX export, the system should set column widths based on content length (up to a maximum).
**Validates: Requirements 6.6**

### Property 31: Export Field Completeness
*For any* export operation, all attendance fields including optional time fields should be present in the output.
**Validates: Requirements 6.7**

### Property 32: Export Date and Time Formatting
*For any* export operation, dates should be formatted as DD-MM-YYYY and times as HH:MM.
**Validates: Requirements 6.8**

### Property 33: Upload Log Completeness
*For any* completed upload, the UploadLog should contain user, timestamp, filename, success count, update count, and error count.
**Validates: Requirements 7.2**

### Property 34: Upload Error Message Storage
*For any* CSV upload with validation errors, the error messages should be stored in the UploadLog.
**Validates: Requirements 7.3**

### Property 35: Authentication Event Logging
*For any* login attempt (successful or failed), the system should create a log entry with username and outcome.
**Validates: Requirements 7.4**

### Property 36: Permission Denial Logging
*For any* permission denial, the system should log the user, role, and attempted action.
**Validates: Requirements 7.5**

### Property 37: Root Log Access
*For any* log view request by a root user, the system should display upload logs from all companies.
**Validates: Requirements 7.6**

### Property 38: Admin Log Filtering
*For any* log view request by an admin user, the system should display only logs from users in their company.
**Validates: Requirements 7.7**

### Property 39: Company Deletion Cascades
*For any* company deletion, all associated attendance records should be deleted, and associated users should have their company field set to NULL.
**Validates: Requirements 8.7, 8.8**

### Property 40: User Deletion Cascades
*For any* user deletion, all associated upload logs should be deleted.
**Validates: Requirements 8.9**

### Property 41: Unauthenticated Access Redirect
*For any* request to a protected view by an unauthenticated user, the system should redirect to the login page.
**Validates: Requirements 9.2**

### Property 42: Error Message Display
*For any* view error, the system should display a user-friendly message using the Django messages framework.
**Validates: Requirements 9.6**

### Property 43: CSV Whitespace Sanitization
*For any* CSV input data, the system should strip leading and trailing whitespace before validation and storage.
**Validates: Requirements 10.2**

### Property 44: CSRF Protection
*For any* POST request without a valid CSRF token, the system should reject the request with a 403 error.
**Validates: Requirements 10.3**

### Property 45: Password Hashing
*For any* user password, the system should store only the hashed version, never plaintext.
**Validates: Requirements 10.4**

### Property 46: Empty Field Validation
*For any* employee number or name that is empty or whitespace-only after stripping, the system should reject it with a validation error.
**Validates: Requirements 10.6**

### Property 47: Descriptive Error Messages
*For any* validation error, the system should return a message that clearly describes what went wrong.
**Validates: Requirements 10.7**

### Property 48: Dual Logging Output
*For any* log event, the system should write to both console and file outputs.
**Validates: Requirements 11.3**

### Property 49: Database Error Handling
*For any* database error during an operation, the system should log the error and display a user-friendly message without crashing.
**Validates: Requirements 12.2**

### Property 50: File Upload Error Display
*For any* file upload validation failure, the system should display the specific validation error to the user.
**Validates: Requirements 12.3**

### Property 51: CSV Exception Handling
*For any* exception during CSV processing, the system should catch it, log it, and continue processing without crashing.
**Validates: Requirements 12.4**

## Error Handling

### Error Handling Strategy

The system implements a multi-layered error handling approach:

1. **Validation Layer**: Catch errors at input validation (forms, CSV processor)
2. **Business Logic Layer**: Handle domain-specific errors (permissions, business rules)
3. **Data Layer**: Manage database errors (integrity constraints, connection issues)
4. **Presentation Layer**: Display user-friendly error messages

### Error Types and Handling

#### 1. Validation Errors

**Source**: Form validation, CSV processing
**Handling**:
- Collect all validation errors
- Display to user with specific field/row information
- Log validation failures
- Do not save invalid data

**Example**:
```python
# Form validation
def clean_date(self):
    date_value = self.cleaned_data.get('date')
    if date_value and date_value > date.today():
        raise forms.ValidationError('Date cannot be in the future.')
    return date_value

# CSV validation
if not self.validate_status(row['STATUS']):
    errors.append(f"Row {row_number}: Invalid status value")
```

#### 2. Permission Errors

**Source**: Role-based access control decorators
**Handling**:
- Return HTTP 403 Forbidden
- Log permission denial with user and attempted action
- Display user-friendly error message
- Redirect to safe page

**Example**:
```python
@role_required(['root', 'admin'])
def upload_csv_view(request):
    # If user doesn't have role, decorator returns 403
    # and logs: "Permission denied: User X (role: user1) 
    # attempted to access upload_csv_view"
```

#### 3. Authentication Errors

**Source**: Login attempts, session validation
**Handling**:
- Display error message on login page
- Log failed authentication attempts
- Do not reveal whether username or password was wrong
- Rate limiting (should be implemented in production)

**Example**:
```python
user = authenticate(request, username=username, password=password)
if user is not None:
    login(request, user)
    logger.info(f'Successful login: {user.username}')
else:
    logger.warning(f'Failed login attempt for username: {username}')
    messages.error(request, 'Invalid username or password.')
```

#### 4. Database Errors

**Source**: ORM operations, constraint violations
**Handling**:
- Catch Django database exceptions
- Log full error details
- Display generic user-friendly message
- Rollback transaction if needed

**Example**:
```python
try:
    record, created = AttendanceRecord.objects.update_or_create(
        ep_no=data['ep_no'],
        date=data['date'],
        defaults=data
    )
except Exception as e:
    logger.error(f'Database error: {str(e)}')
    raise Exception(f"Error saving record: {str(e)}")
```

#### 5. File Processing Errors

**Source**: CSV upload, file validation
**Handling**:
- Validate file extension before processing
- Catch CSV parsing errors
- Continue processing valid rows even if some fail
- Collect all errors for reporting
- Create upload log with error details

**Example**:
```python
if not csv_file.name.endswith('.csv'):
    logger.warning(f'Invalid file upload: {csv_file.name}')
    messages.error(request, 'Please upload a valid CSV file.')
    return redirect('core:upload')
```

#### 6. HTTP Errors

**Source**: Invalid URLs, server errors
**Handling**:
- Custom error pages for 403, 404, 500
- Log 500 errors with full traceback
- Display user-friendly error messages
- Provide navigation back to safe pages

**Example**:
```python
# In urls.py
handler404 = 'core.views.handler404'
handler403 = 'core.views.handler403'
handler500 = 'core.views.handler500'

# In views.py
def handler404(request, exception):
    return render(request, '404.html', status=404)
```

### Error Logging

All errors are logged with appropriate severity levels:

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages (successful operations)
- **WARNING**: Warning messages (failed login, invalid file)
- **ERROR**: Error messages (database errors, processing failures)
- **CRITICAL**: Critical errors (system failures)

**Log Format**:
```
{levelname} {asctime} {module} {message}
Example: ERROR 2024-01-15 10:30:45 views Database error: IntegrityError at /upload/
```

**Log Destinations**:
- Console: All levels (development)
- File: INFO and above (production)
- File location: `logs/attendance_system.log`

### User-Facing Error Messages

**Principles**:
1. **Clear**: Explain what went wrong
2. **Actionable**: Tell user how to fix it
3. **Non-technical**: Avoid technical jargon
4. **Secure**: Don't reveal sensitive system information

**Examples**:
- ✅ "Please upload a valid CSV file."
- ✅ "Date cannot be in the future."
- ✅ "You do not have permission to access this page."
- ❌ "IntegrityError: duplicate key value violates unique constraint"
- ❌ "NoneType object has no attribute 'company'"

## Testing Strategy

### Overview

The testing strategy combines unit testing for specific functionality and property-based testing for universal correctness properties. This dual approach ensures both concrete examples work correctly and general properties hold across all inputs.

### Testing Framework

**Unit Testing**: Django's built-in test framework (based on unittest)
**Property-Based Testing**: Hypothesis library for Python
**Test Database**: SQLite in-memory database for speed
**Coverage Tool**: coverage.py for code coverage analysis

### Unit Testing Approach

Unit tests verify specific examples, edge cases, and integration points:

**Model Tests**:
- Test model creation and validation
- Test unique constraints
- Test foreign key relationships
- Test model methods and properties

**View Tests**:
- Test authentication and authorization
- Test form submission and validation
- Test redirect behavior
- Test context data

**Form Tests**:
- Test field validation
- Test custom clean methods
- Test form submission

**CSV Processor Tests**:
- Test date/time parsing
- Test validation logic
- Test error collection
- Test upsert behavior

**Example Unit Test**:
```python
class AttendanceRecordModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company")
    
    def test_unique_constraint(self):
        """Test that duplicate ep_no + date raises error"""
        AttendanceRecord.objects.create(
            ep_no="E001",
            ep_name="John Doe",
            company=self.company,
            date="2024-01-15",
            shift="Day",
            overstay="0",
            status="P"
        )
        
        with self.assertRaises(IntegrityError):
            AttendanceRecord.objects.create(
                ep_no="E001",
                ep_name="John Doe",
                company=self.company,
                date="2024-01-15",
                shift="Day",
                overstay="0",
                status="P"
            )
```

### Property-Based Testing Approach

Property-based tests verify universal properties across randomly generated inputs:

**Configuration**:
- Minimum 100 iterations per property test
- Use Hypothesis strategies for data generation
- Shrink failing examples to minimal cases

**Property Test Structure**:
1. Generate random valid inputs
2. Execute system operation
3. Assert property holds
4. Tag with property number from design doc

**Example Property Test**:
```python
from hypothesis import given, strategies as st
from hypothesis.extra.django import TestCase

class AttendancePropertyTests(TestCase):
    @given(
        ep_no=st.text(min_size=1, max_size=50),
        ep_name=st.text(min_size=1, max_size=255),
        date=st.dates(max_value=date.today())
    )
    @settings(max_examples=100)
    def test_property_20_future_date_rejection(self, ep_no, ep_name, date):
        """
        Feature: backend-architecture-documentation, Property 20: Future Date Rejection
        For any attendance record with a future date, system should reject it
        """
        company = Company.objects.create(name="Test Co")
        
        # Test with future date
        future_date = date.today() + timedelta(days=1)
        
        with self.assertRaises(ValidationError):
            record = AttendanceRecord(
                ep_no=ep_no,
                ep_name=ep_name,
                company=company,
                date=future_date,
                shift="Day",
                overstay="0",
                status="P"
            )
            record.full_clean()  # Trigger validation
```

### Test Organization

```
core/
├── tests/
│   ├── __init__.py
│   ├── test_models.py          # Model unit tests
│   ├── test_views.py           # View unit tests
│   ├── test_forms.py           # Form unit tests
│   ├── test_csv_processor.py  # CSV processor unit tests
│   ├── test_decorators.py     # Decorator unit tests
│   └── test_properties.py     # Property-based tests
```

### Test Coverage Goals

- **Overall Coverage**: Minimum 80%
- **Critical Paths**: 100% (authentication, authorization, data validation)
- **Business Logic**: 90% (CSV processing, data operations)
- **Views**: 85% (all user-facing functionality)
- **Models**: 90% (data integrity and relationships)

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test core.tests.test_models

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Run property tests only
python manage.py test core.tests.test_properties
```

### Continuous Integration

Tests should run automatically on:
- Every commit to main branch
- Every pull request
- Nightly builds for extended property testing

### Test Data Management

**Fixtures**: Use Django fixtures for consistent test data
**Factories**: Use factory_boy for generating test objects
**Cleanup**: Django's TestCase handles database cleanup automatically

### Performance Testing

While not part of the core test suite, performance should be monitored:
- CSV processing speed (records per second)
- Query performance (response time)
- Export generation time
- Pagination performance with large datasets

## API Documentation

### URL Structure

All URLs follow RESTful conventions where applicable:

```
/                                    # Dashboard (GET)
/login/                              # Login (GET, POST)
/logout/                             # Logout (GET, POST)
/attendance/                         # List records (GET)
/attendance/export/                  # Export XLSX (GET)
/attendance/<id>/edit/               # Edit record (GET, POST)
/attendance/<id>/delete/             # Delete record (POST)
/upload/                             # Upload CSV (GET, POST)
/upload/logs/                        # View upload logs (GET)
/upload/template/                    # Download template (GET)
/export/                             # Export CSV (GET)
/users/                              # List users (GET)
/users/create/                       # Create user (GET, POST)
/users/<id>/edit/                    # Edit user (GET, POST)
/users/<id>/delete/                  # Delete user (GET, POST)
```

### Endpoint Details

#### Authentication Endpoints

**POST /login/**
- **Purpose**: Authenticate user
- **Parameters**: username, password
- **Returns**: Redirect to dashboard or login with errors
- **Permissions**: Public

**GET /logout/**
- **Purpose**: End session
- **Returns**: Redirect to login
- **Permissions**: Authenticated

#### Dashboard Endpoint

**GET /**
- **Purpose**: Display system overview
- **Returns**: HTML with statistics
- **Permissions**: Authenticated
- **Context**:
  - total_records: int
  - total_companies: int
  - recent_uploads: QuerySet[UploadLog]

#### Attendance Endpoints

**GET /attendance/**
- **Purpose**: List attendance records
- **Query Parameters**:
  - date_from: YYYY-MM-DD
  - date_to: YYYY-MM-DD
  - company: int (Root only)
  - ep_no: string
  - status: string
  - page: int
- **Returns**: HTML with paginated records
- **Permissions**: Authenticated, company access required

**GET /attendance/export/**
- **Purpose**: Export to XLSX
- **Query Parameters**: Same as list view
- **Returns**: XLSX file download
- **Permissions**: Authenticated, company access required

**GET /attendance/<id>/edit/**
- **Purpose**: Show edit form
- **Returns**: HTML with form
- **Permissions**: Root or Admin

**POST /attendance/<id>/edit/**
- **Purpose**: Save changes
- **Parameters**: All attendance fields
- **Returns**: Redirect to list or form with errors
- **Permissions**: Root or Admin

**POST /attendance/<id>/delete/**
- **Purpose**: Delete record
- **Returns**: Redirect to list
- **Permissions**: Root or Admin

#### Upload Endpoints

**GET /upload/**
- **Purpose**: Show upload form
- **Returns**: HTML with form and recent logs
- **Permissions**: Root or Admin

**POST /upload/**
- **Purpose**: Process CSV file
- **Parameters**: csv_file (multipart/form-data)
- **Returns**: Redirect to upload page with messages
- **Permissions**: Root or Admin

**GET /upload/template/**
- **Purpose**: Download CSV template
- **Returns**: CSV file
- **Permissions**: Root or Admin

**GET /upload/logs/**
- **Purpose**: View upload history
- **Query Parameters**: page (int)
- **Returns**: HTML with paginated logs
- **Permissions**: Root or Admin

#### Export Endpoints

**GET /export/**
- **Purpose**: Export to CSV
- **Query Parameters**: Same as list view
- **Returns**: CSV file download
- **Permissions**: Authenticated

#### User Management Endpoints

**GET /users/**
- **Purpose**: List users
- **Returns**: HTML with user list
- **Permissions**: Root or Admin

**GET /users/create/**
- **Purpose**: Show create form
- **Returns**: HTML with form
- **Permissions**: Root or Admin

**POST /users/create/**
- **Purpose**: Create user
- **Parameters**: username, role, company, password
- **Returns**: Redirect to list or form with errors
- **Permissions**: Root or Admin

**GET /users/<id>/edit/**
- **Purpose**: Show edit form
- **Returns**: HTML with form
- **Permissions**: Root or Admin

**POST /users/<id>/edit/**
- **Purpose**: Save changes
- **Parameters**: username, role, company, password (optional)
- **Returns**: Redirect to list or form with errors
- **Permissions**: Root or Admin

**GET /users/<id>/delete/**
- **Purpose**: Show confirmation
- **Returns**: HTML with confirmation form
- **Permissions**: Root only

**POST /users/<id>/delete/**
- **Purpose**: Delete user
- **Returns**: Redirect to list
- **Permissions**: Root only

### Response Formats

**HTML Responses**:
- All views return rendered HTML templates
- Use Django messages framework for user feedback
- Include CSRF tokens in all forms

**File Downloads**:
- CSV: text/csv with Content-Disposition header
- XLSX: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

**Error Responses**:
- 403: Custom forbidden page
- 404: Custom not found page
- 500: Custom server error page

### Authentication

**Method**: Django session-based authentication
**Session Cookie**: sessionid (httponly, secure in production)
**CSRF Protection**: Required for all POST requests
**Login Required**: All endpoints except /login/

### Rate Limiting

Not currently implemented but recommended for production:
- Login attempts: 5 per minute per IP
- CSV uploads: 10 per hour per user
- API calls: 100 per minute per user

## Deployment Considerations

### Environment Configuration

**Development**:
- DEBUG = True
- SQLite database
- Console logging
- ALLOWED_HOSTS = ['localhost', '127.0.0.1']

**Production**:
- DEBUG = False
- PostgreSQL database
- File + console logging
- ALLOWED_HOSTS = [your-domain.com]
- SECRET_KEY from environment variable
- HTTPS only
- Secure cookies

### Database Migration

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create initial data
python manage.py create_initial_data
```

### Static Files

```bash
# Collect static files for production
python manage.py collectstatic
```

### Security Checklist

- [ ] Change SECRET_KEY
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS
- [ ] Set secure cookie flags
- [ ] Configure CSRF settings
- [ ] Set up rate limiting
- [ ] Configure firewall
- [ ] Regular security updates
- [ ] Database backups
- [ ] Log monitoring
- [ ] Input validation
- [ ] SQL injection protection (Django ORM)
- [ ] XSS protection (Django templates)

### Performance Optimization

**Database**:
- Use connection pooling
- Add indexes on frequently queried fields
- Use select_related() for foreign keys
- Use prefetch_related() for reverse foreign keys
- Regular VACUUM and ANALYZE

**Caching**:
- Cache dashboard statistics
- Cache company list for filters
- Use Redis for session storage
- Cache static files with CDN

**Query Optimization**:
- Paginate large result sets
- Use database indexes
- Avoid N+1 queries
- Use bulk operations for CSV import

### Monitoring

**Metrics to Track**:
- Request response time
- Database query time
- CSV processing time
- Error rates
- Login success/failure rates
- Active users
- Storage usage

**Logging**:
- Application logs: logs/attendance_system.log
- Web server logs: /var/log/nginx/ or /var/log/apache2/
- Database logs: PostgreSQL logs

### Backup Strategy

**Database Backups**:
- Daily full backups
- Hourly incremental backups
- Retain for 30 days
- Test restore procedures monthly

**File Backups**:
- Static files
- Media files (if any)
- Log files
- Configuration files

### Scaling Considerations

**Horizontal Scaling**:
- Use load balancer
- Shared session storage (Redis)
- Shared file storage (S3, NFS)
- Database replication

**Vertical Scaling**:
- Increase server resources
- Optimize database queries
- Add caching layers
- Use CDN for static files

## Conclusion

This backend architecture provides a robust, secure, and scalable foundation for the Attendance Management System. The multi-tenant design ensures data isolation, role-based access control provides appropriate permissions, and comprehensive validation ensures data integrity. The system is built on Django best practices and is ready for production deployment with proper configuration.

### Key Strengths

1. **Security First**: Multiple layers of authentication, authorization, and validation
2. **Data Integrity**: Comprehensive validation at all levels
3. **Audit Trail**: Complete logging of all operations
4. **Scalability**: Multi-tenant architecture supports growth
5. **Maintainability**: Clean separation of concerns, well-documented code
6. **Testability**: Comprehensive test coverage with unit and property-based tests

### Future Enhancements

- REST API for mobile/external integrations
- Real-time notifications
- Advanced reporting and analytics
- Bulk operations UI
- Role customization
- Multi-language support
- Advanced search and filtering
- Data export scheduling
- Integration with HR systems
- Biometric device integration
