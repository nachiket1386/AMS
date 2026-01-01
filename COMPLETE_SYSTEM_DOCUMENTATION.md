# Attendance Management System (AMS)
## Complete System Documentation

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [System Architecture](#system-architecture)
4. [Database Structure](#database-structure)
5. [User Roles & Permissions](#user-roles--permissions)
6. [Core Features](#core-features)
7. [Dashboard Components](#dashboard-components)
8. [Application Logic](#application-logic)
9. [API Endpoints](#api-endpoints)
10. [Installation & Setup](#installation--setup)
11. [Usage Guide](#usage-guide)
12. [Security Features](#security-features)

---

## 1. System Overview

### Purpose
The Attendance Management System (AMS) is a comprehensive web application designed to track, manage, and analyze employee attendance, overtime, regularization requests, and manday summaries for multiple companies and contractors.

### Key Objectives
- Centralized attendance tracking across multiple companies
- Automated overtime calculation and approval workflow
- Regularization request management
- Real-time dashboard analytics
- Role-based access control
- Comprehensive reporting capabilities

### Target Users
- **Root Users**: System administrators with full access
- **Admin Users**: Company administrators managing their organization
- **User1 (Supervisors)**: Limited access to assigned employees
- **Regular Users**: View-only access to specific data

---

## 2. Technology Stack

### Backend
- **Framework**: Django 4.2
- **Language**: Python 3.11+
- **Database**: SQLite (Development) / PostgreSQL (Production Ready)
- **ORM**: Django ORM

### Frontend
- **Template Engine**: Django Templates
- **CSS Framework**: Tailwind CSS
- **JavaScript**: Vanilla JS (minimal)
- **Icons**: SVG Icons

### Additional Libraries
- **openpyxl**: Excel file processing
- **python-dateutil**: Date parsing
- **Pillow**: Image processing

### Development Tools
- **Version Control**: Git
- **Repository**: GitHub
- **IDE**: VS Code / PyCharm

---

## 3. System Architecture

### Application Structure
```
attendance_system/
├── attendance_system/          # Project configuration
│   ├── settings.py            # Django settings
│   ├── urls.py                # Root URL configuration
│   └── wsgi.py                # WSGI configuration
├── core/                      # Main application
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── urls.py                # URL routing
│   ├── forms.py               # Form definitions
│   ├── decorators.py          # Custom decorators
│   ├── csv_processor.py       # CSV processing logic
│   ├── manday_processor.py    # Manday calculations
│   ├── services/              # Business logic services
│   │   ├── access_control_service.py
│   │   ├── data_importer_service.py
│   │   ├── data_validator_service.py
│   │   ├── export_service.py
│   │   ├── file_parser_service.py
│   │   └── permission_service.py
│   ├── templates/             # HTML templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── attendance_list.html
│   │   ├── reports/
│   │   └── ...
│   ├── static/                # Static files (CSS, JS, images)
│   ├── templatetags/          # Custom template filters
│   │   ├── custom_filters.py
│   │   └── attendance_filters.py
│   └── migrations/            # Database migrations
├── media/                     # User uploaded files
├── logs/                      # Application logs
├── db.sqlite3                 # SQLite database
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
```

### Design Patterns
- **MVC Pattern**: Model-View-Controller architecture
- **Service Layer**: Business logic separated into services
- **Decorator Pattern**: Custom decorators for access control
- **Repository Pattern**: Data access through Django ORM

---

## 4. Database Structure

### Entity Relationship Diagram
```
┌─────────────┐         ┌──────────────────┐         ┌─────────────┐
│   Company   │────────<│ AttendanceRecord │>────────│    User     │
└─────────────┘         └──────────────────┘         └─────────────┘
                                 │
                                 │
                        ┌────────┴────────┐
                        │                 │
                ┌───────▼──────┐  ┌──────▼────────┐
                │ RemarkReason │  │ UploadLog     │
                └──────────────┘  └───────────────┘
```

### Core Models

#### 1. User Model
**Purpose**: Authentication and authorization

**Fields**:
- `username` (CharField): Unique username
- `email` (EmailField): User email
- `role` (CharField): User role (root/admin/user1/user)
- `company` (ForeignKey): Associated company
- `assigned_employees` (JSONField): List of assigned EP numbers (for user1)
- `is_active` (BooleanField): Account status
- `date_joined` (DateTimeField): Registration date

**Relationships**:
- One-to-Many with Company
- One-to-Many with UploadLog

**Role Types**:
- `root`: Full system access
- `admin`: Company-level administration
- `user1`: Supervisor with limited employee access
- `user`: Read-only access

---

#### 2. Company Model
**Purpose**: Multi-tenant organization management

**Fields**:
- `name` (CharField): Company name
- `code` (CharField): Unique company code
- `address` (TextField): Company address
- `contact_person` (CharField): Contact person name
- `contact_email` (EmailField): Contact email
- `contact_phone` (CharField): Contact phone
- `is_active` (BooleanField): Company status
- `created_at` (DateTimeField): Creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Relationships**:
- One-to-Many with User
- One-to-Many with AttendanceRecord

---

#### 3. AttendanceRecord Model
**Purpose**: Core attendance tracking

**Fields**:

**Employee Information**:
- `ep_no` (CharField): Employee ID
- `ep_name` (CharField): Employee name
- `company` (ForeignKey): Associated company
- `cont_code` (CharField): Contractor code
- `contract` (CharField): Contract number
- `trade` (CharField): Employee trade/skill

**Date & Time**:
- `date` (DateField): Attendance date
- `shift` (CharField): Shift information
- `in_time` (TimeField): Original clock-in time
- `out_time` (TimeField): Original clock-out time
- `in_time_2` (TimeField): Regularized clock-in time
- `out_time_2` (TimeField): Regularized clock-out time
- `in_time_3` (TimeField): Additional punch time
- `out_time_3` (TimeField): Additional punch time

**Attendance Status**:
- `status` (CharField): P/A/L/PD (Present/Absent/Late/Partial Day)
- `hours` (DecimalField): Total working hours
- `mandays` (DecimalField): Calculated mandays

**Overtime & Regularization**:
- `ot` (DecimalField): Overtime hours
- `overtime` (DecimalField): Approved overtime
- `requested_overtime` (DecimalField): Requested overtime
- `approved_overtime` (DecimalField): Final approved overtime
- `overstay` (CharField): Overstay duration
- `actual_overstay` (CharField): Calculated overstay
- `overtime_to_mandays` (DecimalField): OT converted to mandays

**Request Management**:
- `ot_request_status` (CharField): Approved/Pending/Rejected
- `requested_eic_code` (CharField): Requesting EIC code
- `requested_eic_name` (CharField): Requesting EIC name
- `contractor_ot_reason` (TextField): OT reason
- `contractor_ot_remarks` (TextField): OT remarks

**Manday Calculations**:
- `regular_manday_hr` (DecimalField): Regular manday hours
- `requested_regular_manday_hours` (DecimalField): Requested hours
- `approved_regular_manday_hours` (DecimalField): Approved hours

**Metadata**:
- `remarks` (TextField): Additional remarks
- `created_at` (DateTimeField): Record creation
- `updated_at` (DateTimeField): Last update

**Indexes**:
- `ep_no`, `date` (Composite index for fast lookups)
- `company`, `date` (Company-wise filtering)
- `ot_request_status` (Status filtering)

---

#### 4. RemarkReason Model
**Purpose**: Predefined remark templates

**Fields**:
- `reason` (CharField): Remark text
- `category` (CharField): Remark category
- `is_active` (BooleanField): Active status
- `created_by` (ForeignKey): Creator user
- `created_at` (DateTimeField): Creation timestamp

---

#### 5. AttendanceRemark Model
**Purpose**: Track remarks on attendance records

**Fields**:
- `attendance_record` (ForeignKey): Related attendance
- `remark_reason` (ForeignKey): Selected reason
- `custom_remark` (TextField): Custom text
- `added_by` (ForeignKey): User who added
- `added_at` (DateTimeField): Timestamp

---

#### 6. UploadLog Model
**Purpose**: Track file uploads and processing

**Fields**:
- `user` (ForeignKey): Uploader
- `filename` (CharField): Uploaded file name
- `upload_date` (DateTimeField): Upload timestamp
- `success_count` (IntegerField): Successfully processed records
- `updated_count` (IntegerField): Updated records
- `error_count` (IntegerField): Failed records
- `error_messages` (TextField): Error details
- `file_type` (CharField): CSV/Excel type

---

## 5. User Roles & Permissions

### Role Hierarchy
```
Root (Superuser)
    ├── Full system access
    ├── Manage all companies
    ├── Manage all users
    └── System configuration

Admin (Company Admin)
    ├── Manage company data
    ├── View all company employees
    ├── Upload attendance files
    └── Generate reports

User1 (Supervisor)
    ├── View assigned employees only
    ├── Limited reporting
    └── No upload permissions

User (Read-only)
    ├── View own data
    └── Basic reports
```

### Permission Matrix

| Feature | Root | Admin | User1 | User |
|---------|------|-------|-------|------|
| Dashboard Access | ✅ | ✅ | ✅ | ✅ |
| View All Attendance | ✅ | ✅ (Company) | ❌ | ❌ |
| View Assigned Employees | ✅ | ✅ | ✅ | ❌ |
| Upload CSV/Excel | ✅ | ✅ | ❌ | ❌ |
| Edit Records | ✅ | ✅ | ❌ | ❌ |
| Delete Records | ✅ | ✅ | ❌ | ❌ |
| Approve OT | ✅ | ✅ | ❌ | ❌ |
| Approve Regularization | ✅ | ✅ | ❌ | ❌ |
| Manage Users | ✅ | ✅ (Company) | ❌ | ❌ |
| System Settings | ✅ | ❌ | ❌ | ❌ |
| Export Reports | ✅ | ✅ | ✅ | ❌ |

---

## 6. Core Features

### 6.1 Attendance Tracking
**Description**: Record and manage daily employee attendance

**Capabilities**:
- Multiple punch-in/out times
- Shift-based tracking
- Late arrival detection
- Early departure tracking
- Partial day calculations
- Absence marking

**Business Rules**:
- Minimum 4 hours for half day (0.5 manday)
- 8+ hours for full day (1.0 manday)
- Overtime calculated beyond shift hours
- Overstay tracked separately

---

### 6.2 Overtime Management
**Description**: Request, approve, and track overtime hours

**Workflow**:
1. System detects overtime (hours beyond shift)
2. Contractor/EIC submits OT request
3. Admin reviews and approves/rejects
4. Approved OT added to mandays
5. Reports generated for billing

**Features**:
- Automatic OT detection
- Request status tracking (Pending/Approved/Rejected)
- EIC-wise OT summary
- Reason and remarks capture
- Approval workflow

---

### 6.3 Regularization
**Description**: Correct punch time errors

**Use Cases**:
- Missed punch-in/out
- Wrong punch time
- System errors
- Manual corrections

**Process**:
1. Employee/Supervisor identifies error
2. Submits regularization request
3. Provides old and new times
4. Admin approves/rejects
5. System updates attendance

**Fields**:
- Old In/Out times
- New In/Out times
- Reason for change
- Approval status

---

### 6.4 Manday Calculations
**Description**: Convert attendance to billable mandays

**Formula**:
```
Mandays = (Working Hours / Standard Hours) + (Approved OT / Standard Hours)

Where:
- Standard Hours = 8 hours (configurable)
- Working Hours = Out Time - In Time - Breaks
- Approved OT = Overtime hours approved by admin
```

**Examples**:
- 8 hours work = 1.0 manday
- 4 hours work = 0.5 manday
- 8 hours + 2 hours OT = 1.25 mandays
- 6 hours work = 0.75 manday

---

### 6.5 File Upload & Processing
**Description**: Bulk import attendance data

**Supported Formats**:
- CSV files
- Excel (.xls, .xlsx)
- Crystal Reports exports

**Processing Steps**:
1. File validation
2. Data parsing
3. Field mapping
4. Duplicate detection
5. Data validation
6. Database insertion
7. Error reporting

**Features**:
- Real-time progress tracking
- Error logging
- Duplicate handling (update existing)
- Batch processing
- Rollback on critical errors

---

### 6.6 Reporting System
**Description**: Generate comprehensive reports

**Available Reports**:

1. **Attendance Report**
   - Date range filtering
   - Employee-wise summary
   - Status breakdown
   - Export to Excel/PDF

2. **Overtime Report**
   - EIC-wise summary
   - Approved vs Pending
   - Date range analysis
   - Cost calculations

3. **Regularization Report**
   - Pending requests
   - Approval history
   - Reason analysis

4. **Partial Day Report**
   - Half-day tracking
   - Deduction summary
   - EIC-wise breakdown

5. **ARC Summary**
   - Trade-wise analysis
   - Contractor comparison
   - Manday totals
   - Pivot table view

---

## 7. Dashboard Components

### 7.1 Dashboard Layout
**Design**: Responsive grid layout with 5 main widgets

**Structure**:
```
┌─────────────────────────────────────────────────┐
│  Dashboard Header (Date, User Info)             │
├─────────────┬─────────────┬─────────────────────┤
│ Attendance  │  Overtime   │  Regularization     │
│  Calendar   │   Summary   │     Summary         │
│             │             │                     │
├─────────────┴─────────────┴─────────────────────┤
│  Partial Day Report                             │
├─────────────────────────────────────────────────┤
│  ARC Summary (Full Width Pivot Table)           │
└─────────────────────────────────────────────────┘
```

---

### 7.2 Attendance Calendar Widget
**Purpose**: Visual monthly attendance view

**Features**:
- EP number search
- Month selection
- Color-coded days:
  - 🟢 Green: Present
  - 🔴 Red: Absent
  - 🟡 Yellow: Half Day/Late
  - ⚪ White: No data
- Hover tooltips with details
- Summary cards:
  - Present days count
  - Exception days count
  - Total logged days

**Interaction**:
- Search by EP number
- Select month/year
- Click day for details
- Visual status indicators

---

### 7.3 Overtime Summary Widget
**Purpose**: Track OT requests by EIC

**Display**:
- Table format
- Columns: EIC Name, Approved, Pending, Total
- Grand total row
- Color-coded status

**Data**:
- Top 10 EICs by request volume
- Real-time status updates
- Clickable rows for details

---

### 7.4 Regularization Summary Widget
**Purpose**: Monitor regularization requests

**Display**:
- Similar to Overtime widget
- EIC-wise breakdown
- Approved/Pending/Total columns
- Grand totals

**Features**:
- Status filtering
- Quick approval access
- Request details on click

---

### 7.5 Partial Day Report Widget
**Purpose**: Track half-day attendance

**Display**:
- EIC Name and Total count
- Compact table view
- Grand total

**Use Case**:
- Monitor partial attendance
- Identify patterns
- Payroll adjustments

---

### 7.6 ARC Summary Widget
**Purpose**: Contractor-wise manday analysis

**Display**:
- Pivot table format
- Rows: Trades (e.g., Operator, Supervisor)
- Columns: Top 7 contractors (by mandays)
- Cells: Manday totals
- Row and column grand totals

**Features**:
- Contractor name display (not codes)
- Sortable columns
- Export capability
- Drill-down to details

**Example**:
```
Trade              | Contractor A | Contractor B | Grand Total
-------------------|--------------|--------------|------------
SR OPERATOR-8HR    |    317.70    |    140.94    |   1419.16
OPERATOR-8HR       |      0.00    |     24.00    |    580.87
SUPERVISOR-8HR     |      0.00    |      0.00    |    198.64
-------------------|--------------|--------------|------------
Grand Total        |    317.70    |    164.94    |   3052.13
```

---

## 8. Application Logic

### 8.1 Authentication Flow
```
1. User visits login page
2. Enters username/password
3. Django authenticates credentials
4. Session created
5. User redirected to dashboard
6. Role-based access applied
```

**Security**:
- CSRF protection
- Password hashing (PBKDF2)
- Session management
- Login required decorators

---

### 8.2 Attendance Processing Logic

**CSV Upload Flow**:
```python
def process_csv(file, user):
    1. Validate file format
    2. Parse CSV rows
    3. For each row:
        a. Extract employee data
        b. Parse date and times
        c. Calculate hours and mandays
        d. Check for duplicates (ep_no + date)
        e. If exists: Update record
        f. If new: Create record
    4. Log results (success/error counts)
    5. Return summary
```

**Manday Calculation**:
```python
def calculate_mandays(in_time, out_time, shift_hours=8):
    working_hours = (out_time - in_time).total_seconds() / 3600
    mandays = working_hours / shift_hours
    
    # Round to 2 decimals
    return round(mandays, 2)
```

**Overtime Detection**:
```python
def detect_overtime(working_hours, shift_hours=8):
    if working_hours > shift_hours:
        overtime = working_hours - shift_hours
        return round(overtime, 2)
    return 0
```

---

### 8.3 Access Control Logic

**User1 (Supervisor) Access**:
```python
def filter_queryset_by_access(queryset, user):
    if user.role == 'user1':
        assigned_eps = user.assigned_employees or []
        if len(assigned_eps) == 0:
            return queryset.none()  # No access
        return queryset.filter(ep_no__in=assigned_eps)
    return queryset  # Full access for admin/root
```

**Decorator Example**:
```python
@role_required(['root', 'admin'])
def upload_csv_view(request):
    # Only root and admin can upload
    pass
```

---

### 8.4 Dashboard Data Aggregation

**EIC Pending Requests**:
```python
eic_pending_requests = AttendanceRecord.objects.filter(
    company=user.company
).exclude(
    requested_eic_name=''
).values('requested_eic_name').annotate(
    approved_count=Count('id', filter=Q(ot_request_status='Approved')),
    pending_count=Count('id', filter=Q(ot_request_status='Pending')),
    total_count=Count('id')
).order_by('-total_count')[:10]
```

**ARC Summary Pivot**:
```python
# Get top 7 contractors by mandays
top_contractors = AttendanceRecord.objects.values(
    'cont_code', 'contract'
).annotate(
    total_mandays=Sum('mandays')
).order_by('-total_mandays')[:7]

# Build pivot: trade -> contractor -> mandays
pivot_data = defaultdict(lambda: defaultdict(float))
for record in records:
    trade = record['trade']
    contractor = record['contract']
    mandays = float(record['mandays'])
    pivot_data[trade][contractor] += mandays
```

---

## 9. API Endpoints

### Authentication
- `GET /login/` - Login page
- `POST /login/` - Authenticate user
- `GET /logout/` - Logout user

### Dashboard
- `GET /` - Main dashboard
- `GET /?calendar_ep=<ep>&calendar_month=<month>` - Calendar view

### Attendance
- `GET /attendance/` - List attendance records
- `GET /attendance/?date_from=<date>&date_to=<date>` - Filter by date
- `GET /attendance/?ep_no=<ep>` - Filter by employee
- `GET /attendance/?status=<status>` - Filter by status
- `GET /attendance/?overstay_filter=<filter>` - Filter by overstay
- `GET /attendance/<id>/` - View record details
- `POST /attendance/<id>/edit/` - Edit record
- `POST /attendance/<id>/delete/` - Delete record

### File Upload
- `GET /upload/` - Upload page
- `POST /upload/` - Process CSV/Excel file
- `GET /upload/progress/` - Get upload progress (AJAX)

### Reports
- `GET /reports/overtime/` - Overtime report
- `GET /reports/regularization/` - Regularization report
- `GET /reports/partial-day/` - Partial day report
- `GET /reports/arc-summary/` - ARC summary report
- `GET /reports/export/` - Export report to Excel

### Admin
- `GET /admin/` - Django admin interface
- `GET /admin/core/attendancerecord/` - Manage attendance
- `GET /admin/core/user/` - Manage users
- `GET /admin/core/company/` - Manage companies

---

## 10. Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git
- Virtual environment tool (venv/virtualenv)

### Step 1: Clone Repository
```bash
git clone https://github.com/nachiket1386/planning-hub.git
cd planning-hub
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Step 5: Create Initial Data
```bash
# Create a company
python manage.py shell
>>> from core.models import Company
>>> company = Company.objects.create(
...     name="Test Company",
...     code="TC001",
...     is_active=True
... )
>>> exit()
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

### Step 7: Access Application
- URL: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Login with superuser credentials

---

## 11. Usage Guide

### For Root Users

**1. Initial Setup**:
- Create companies
- Create admin users for each company
- Configure system settings

**2. User Management**:
- Go to Admin panel
- Create users with appropriate roles
- Assign companies to users
- Set permissions

**3. Data Management**:
- Upload attendance files
- Monitor processing logs
- Handle errors
- Generate reports

---

### For Admin Users

**1. Daily Operations**:
- Upload daily attendance CSV
- Review upload logs
- Check for errors
- Verify data accuracy

**2. Approval Workflow**:
- Review OT requests
- Approve/reject regularizations
- Add remarks to records
- Generate daily reports

**3. Reporting**:
- Generate monthly reports
- Export to Excel
- Analyze trends
- Share with stakeholders

---

### For User1 (Supervisors)

**1. Employee Monitoring**:
- View assigned employees
- Check attendance status
- Review exceptions
- Generate team reports

**2. Limited Actions**:
- View-only access
- Export assigned employee data
- No approval permissions

---

## 12. Security Features

### Authentication
- Session-based authentication
- Password hashing (PBKDF2_SHA256)
- Login required for all views
- CSRF protection on forms

### Authorization
- Role-based access control (RBAC)
- Custom decorators for permissions
- Company-level data isolation
- Employee-level access for User1

### Data Protection
- SQL injection prevention (ORM)
- XSS protection (template escaping)
- CSRF tokens on all forms
- Secure session management

### Audit Trail
- Upload logs with timestamps
- User action tracking
- Error logging
- Change history

---

## 13. Color Scheme & Design

### Brand Colors
- **Dark Blue**: #4A70A9 (Primary)
- **Light Blue**: #8FABD4 (Secondary)
- **Cream**: #EFECE3 (Background)
- **Black**: #000000 (Text)

### Status Colors
- **Green**: #22c55e (Present/Approved)
- **Red**: #ef4444 (Absent/Rejected)
- **Yellow**: #eab308 (Pending/Warning)
- **Gray**: #9ca3af (Inactive/No Data)

### Typography
- **Font Family**: System fonts (sans-serif)
- **Headings**: Bold, 16-24px
- **Body**: Regular, 11-14px
- **Small Text**: 9-10px

---

## 14. Future Enhancements

### Planned Features
1. **Mobile App**: React Native mobile application
2. **Biometric Integration**: Fingerprint/face recognition
3. **Real-time Notifications**: Push notifications for approvals
4. **Advanced Analytics**: ML-based attendance predictions
5. **Payroll Integration**: Direct payroll system connection
6. **Multi-language Support**: Internationalization
7. **API Development**: RESTful API for third-party integrations
8. **Geofencing**: Location-based attendance
9. **Shift Scheduling**: Automated shift management
10. **Leave Management**: Integrated leave tracking

---

## 15. Troubleshooting

### Common Issues

**1. Database Locked Error**:
```bash
# Solution: Close all connections
python manage.py migrate --run-syncdb
```

**2. Static Files Not Loading**:
```bash
# Solution: Collect static files
python manage.py collectstatic
```

**3. Permission Denied**:
- Check user role
- Verify company assignment
- Check assigned_employees for User1

**4. Upload Errors**:
- Verify file format (CSV/Excel)
- Check column headers
- Validate date formats
- Review error logs

---

## 16. Support & Maintenance

### Logging
- Location: `logs/attendance_system.log`
- Levels: DEBUG, INFO, WARNING, ERROR
- Rotation: Daily

### Backup
- Database: Daily automated backup
- Media files: Weekly backup
- Configuration: Version controlled

### Monitoring
- Server uptime
- Database performance
- Error rates
- User activity

---

## 17. License & Credits

### License
Proprietary - All rights reserved

### Credits
- **Developer**: Nachiket Patel
- **Framework**: Django
- **UI Framework**: Tailwind CSS
- **Database**: SQLite/PostgreSQL

---

## 18. Contact Information

### Support
- **Email**: support@example.com
- **GitHub**: https://github.com/nachiket1386/planning-hub
- **Documentation**: This file

### Repository
- **URL**: https://github.com/nachiket1386/planning-hub
- **Branch**: main
- **Version**: 1.0.0

---

**Document Version**: 1.0
**Last Updated**: January 1, 2026
**Status**: Production Ready

---

*End of Documentation*
