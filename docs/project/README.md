# Attendance Management System

Multi-user company data management system with CSV upload functionality built with Django and modern UI design.

## Features

- **Role-Based Access Control**: Root, Admin, and User1 roles with permission enforcement
- **CSV Upload**: Upload attendance data with comprehensive validation
- **Data Management**: View, edit, delete attendance records with company-based filtering
- **Export**: Download filtered or complete data as CSV
- **Upload Logs**: Track all uploads with success/error counts and detailed error messages
- **User Management**: Create and manage users with role-based restrictions
- **Error Handling**: Custom 404, 403, and 500 error pages
- **Logging**: Comprehensive logging for authentication, uploads, and permission violations
- **Form Validation**: Client and server-side validation with helpful error messages
- **Testing**: 26 unit and integration tests with 100% pass rate
- **Modern UI**: Tailwind CSS with responsive design and custom color palette
- **Mobile-Friendly**: Bottom navigation and card-based layouts for all screen sizes

## Tech Stack

- Backend: Django (Python)
- Database: SQLite
- Frontend: Tailwind CSS, HTML, JavaScript
- Font: Inter (Google Fonts)
- Icons: SVG inline icons

## Installation

1. Install dependencies:
```bash
pip install django
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create initial data:
```bash
python manage.py create_initial_data
```

## Usage

### Start the server:
```bash
python manage.py runserver
```

### Access the application:
Open browser: http://127.0.0.1:8000

### Login Credentials:

**Root User** (Full access):
- Username: `root`
- Password: `root123`

**Admin User** (Company-specific access):
- Username: `admin`
- Password: `admin123`
- Company: Sample Company

**User1** (View-only access):
- Username: `user1`
- Password: `user123`
- Company: Sample Company

## CSV Upload Format

### Required Columns:
- EP NO (Employee Number)
- EP NAME (Employee Name)
- COMPANY NAME
- DATE (YYYY-MM-DD)
- SHIFT
- OVERSTAY
- STATUS (P, A, PH, -0.5, -1)

### Optional Columns:
- IN, OUT (HH:MM)
- IN (2), OUT (2) (HH:MM)
- IN (3), OUT (3) (HH:MM)
- OVERTIME (HH:MM)
- OVERTIME TO MANDAYS (HH:MM)

### Sample CSV:
A sample CSV file `sample_attendance.csv` is included in the project root.

## User Roles & Permissions

| Action | Root | Admin | User1 |
|--------|------|-------|-------|
| Upload CSV | ✅ All companies | ✅ Own company | ❌ |
| View Data | ✅ All companies | ✅ Own company | ✅ Own company |
| Edit/Delete | ✅ All companies | ✅ Own company | ❌ |
| Manage Users | ✅ All roles | ✅ User1 only | ❌ |
| Export Data | ✅ | ✅ | ✅ |

## Key Features

### CSV Validation:
- Mandatory field checks
- Date format validation (YYYY-MM-DD)
- Time format validation (HH:MM)
- STATUS value validation
- Future date prevention
- Duplicate handling (updates existing records)

### Upload Logs:
- Tracks who uploaded
- Records success/updated/error counts
- Stores error messages for debugging

### Data Export:
- Export filtered or complete data
- CSV format compatible with upload

## Admin Panel

Access Django admin: http://127.0.0.1:8000/admin
- Username: `root`
- Password: `root123`

## Project Structure

```
attendance_system/
├── attendance_system/      # Django project settings
│   ├── settings.py        # Configuration
│   ├── urls.py            # Root URL routing
│   └── wsgi.py            # WSGI application
├── core/                  # Main application
│   ├── models.py          # Database models
│   ├── views.py           # Business logic
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin configuration
│   ├── forms.py           # Form definitions
│   ├── decorators.py      # Permission decorators
│   ├── csv_processor.py   # CSV validation
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JavaScript
│   ├── tests.py           # Unit & integration tests
│   └── management/        # Management commands
├── db.sqlite3             # SQLite database
├── sample_attendance.csv  # Sample CSV file
├── manage.py              # Django management script
└── README.md              # This file
```

## Running Tests

The project includes 26 comprehensive tests covering:
- CSV processor validation (date, time, status)
- Model creation and constraints
- Authentication workflows
- Complete upload workflows for all roles
- Data management (view, edit, delete)
- User management workflows
- Export functionality
- Permission enforcement

Run all tests:
```bash
python manage.py test
```

Run specific test class:
```bash
python manage.py test core.tests.CSVProcessorTestCase
python manage.py test core.tests.IntegrationTestCase
python manage.py test core.tests.AuthenticationTestCase
```

Run with verbose output:
```bash
python manage.py test --verbosity=2
```

## Development

### Create a new superuser:
```bash
python manage.py createsuperuser
```

### Make migrations after model changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collect static files (for production):
```bash
python manage.py collectstatic
```

## Design

The application features a modern, app-like design with:
- **Custom Color Palette**: Cream (#EFECE3), Light Blue (#8FABD4), Dark Blue (#4A70A9), Black (#000000)
- **Responsive Layout**: Mobile-first design with bottom navigation
- **Card-Based UI**: Rounded corners and clean borders
- **Smooth Transitions**: Hover effects and focus states
- **Icon Integration**: SVG icons throughout the interface

## Logging

The system logs important events to both console and file (`logs/attendance_system.log`):
- **Authentication**: Successful/failed login attempts, logouts
- **CSV Processing**: Upload start, completion, errors
- **Permission Violations**: Unauthorized access attempts

View logs:
```bash
# View recent logs
tail -f logs/attendance_system.log

# Search for errors
grep ERROR logs/attendance_system.log

# Search for specific user activity
grep "username" logs/attendance_system.log
```

## Notes

- Duplicate records (same EP NO + DATE) are automatically updated
- All uploads are logged for audit purposes with detailed error tracking
- Admin users can only manage their assigned company
- Root user has unrestricted access to all data
- Form validation prevents invalid data entry with helpful error messages
- Custom error pages (404, 403, 500) provide user-friendly error handling
- The system uses SQLite for simplicity; for production, consider PostgreSQL or MySQL
- Mobile-responsive design works on all screen sizes
- Comprehensive test coverage ensures reliability

## Security Considerations

- Change SECRET_KEY in production
- Set DEBUG = False in production
- Configure ALLOWED_HOSTS properly
- Use environment variables for sensitive data
- Implement HTTPS in production
- Regular database backups recommended

## License

This project is for educational/demonstration purposes.
