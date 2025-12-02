# System Architecture

## Overview

The Django Attendance Management System follows a traditional Django MVC (Model-View-Controller) architecture with service layer patterns for complex business logic.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Templates  │  │     CSS      │  │  JavaScript  │     │
│  │  (Django)    │  │  (Tailwind)  │  │   (Vanilla)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Views     │  │     Forms    │  │  Decorators  │     │
│  │  (views.py)  │  │  (forms.py)  │  │(decorators.py│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                         SERVICE LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Access    │  │   Request    │  │    Backup    │     │
│  │   Control    │  │   Approval   │  │   Service    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                          DATA LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Models    │  │   Database   │  │  CSV/Excel   │     │
│  │  (models.py) │  │   (SQLite)   │  │  Processor   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Backend
- **Framework**: Django 4.2.7
- **Language**: Python 3.x
- **Database**: SQLite (development), PostgreSQL (production recommended)
- **ORM**: Django ORM

### Frontend
- **CSS Framework**: TailwindCSS 3.4.1 (CDN)
- **JavaScript**: Vanilla JS (no frameworks)
- **Icons**: Heroicons (SVG)
- **Fonts**: Inter (Google Fonts)

### Libraries
- **openpyxl**: Excel file generation
- **pandas**: CSV processing
- **Django built-ins**: Authentication, sessions, messages

---

## Project Structure

```
attendance_system/
├── attendance_system/          # Project configuration
│   ├── settings.py            # Django settings
│   ├── urls.py                # Root URL configuration
│   ├── wsgi.py                # WSGI application
│   └── asgi.py                # ASGI application
│
├── core/                       # Main application
│   ├── models.py              # Data models
│   ├── views.py               # View functions
│   ├── forms.py               # Form definitions
│   ├── urls.py                # URL patterns
│   ├── decorators.py          # Custom decorators
│   ├── csv_processor.py       # CSV processing logic
│   │
│   ├── services/              # Business logic layer
│   │   ├── access_control_service.py
│   │   ├── request_approval_service.py
│   │   └── backup_service.py
│   │
│   ├── templates/             # HTML templates
│   │   ├── base.html          # Base template
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── attendance_list.html
│   │   ├── user_list.html
│   │   ├── 403.html           # Error pages
│   │   └── 403_csrf.html
│   │
│   ├── static/                # Static files
│   │   └── (empty - using CDN)
│   │
│   ├── tests/                 # Test files
│   │   ├── test_access_control_service.py
│   │   ├── test_request_approval_service.py
│   │   └── test_property_request_approval.py
│   │
│   └── management/            # Custom commands
│       └── commands/
│
├── docs/                       # Documentation
├── logs/                       # Application logs
├── prototype/                  # This documentation
├── db.sqlite3                 # Database file
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
```

---

## Design Patterns

### 1. Model-View-Template (MVT)
Django's implementation of MVC:
- **Model**: Data layer (models.py)
- **View**: Business logic (views.py)
- **Template**: Presentation (templates/)

### 2. Service Layer Pattern
Complex business logic extracted to services:
- `AccessControlService`: Manages user access to data
- `RequestApprovalService`: Handles request/approval workflow
- `BackupService`: Manages data backup/restore

### 3. Decorator Pattern
Reusable authorization logic:
- `@login_required`: Django built-in
- `@role_required`: Custom role checking
- `@company_access_required`: Company scope validation

### 4. Repository Pattern (Implicit)
Django ORM acts as repository:
- Models provide data access interface
- QuerySets for filtering and aggregation
- Manager methods for custom queries

---

## Data Flow

### 1. Request Flow
```
User Request
    ↓
URL Router (urls.py)
    ↓
Middleware (CSRF, Auth, Session)
    ↓
Decorator (@login_required, @role_required)
    ↓
View Function (views.py)
    ↓
Service Layer (if needed)
    ↓
Model/Database (models.py)
    ↓
Template Rendering (templates/)
    ↓
HTTP Response
```

### 2. Authentication Flow
```
Login Form Submission
    ↓
authenticate() - Django Auth
    ↓
Check credentials
    ↓
login() - Create session
    ↓
Redirect to dashboard
```

### 3. CSV Upload Flow
```
File Upload
    ↓
Validate file type
    ↓
CSVProcessor.process_csv()
    ↓
Parse rows
    ↓
For each row:
    - Get or create Company
    - Create or update AttendanceRecord
    ↓
Create UploadLog
    ↓
Return results
```

### 4. Access Request Flow
```
User1 submits request
    ↓
Create AccessRequest (pending)
    ↓
Admin views requests
    ↓
Admin approves/rejects
    ↓
Update AccessRequest status
    ↓
Update User1.assigned_employees
    ↓
User1 can now access data
```

---

## Security Architecture

### 1. Authentication
- Django's built-in authentication system
- Session-based (cookies)
- Password hashing (PBKDF2)
- CSRF protection

### 2. Authorization
- Role-based access control (RBAC)
- Custom decorators for view protection
- Company-scoped data access
- Service layer enforces rules

### 3. Data Protection
- SQL injection prevention (ORM)
- XSS protection (template escaping)
- CSRF tokens on all forms
- Secure session cookies

---

## Scalability Considerations

### Current Architecture (Small-Medium Scale)
- SQLite database
- Single server deployment
- Session-based auth
- File-based logging

### Future Scaling Options

#### Database
- Migrate to PostgreSQL
- Add read replicas
- Implement connection pooling
- Use database indexes

#### Caching
- Add Redis for sessions
- Cache query results
- Cache template fragments
- Use CDN for static files

#### Application
- Horizontal scaling (multiple servers)
- Load balancer
- Celery for async tasks
- Message queue (RabbitMQ/Redis)

#### Storage
- Move to S3 for file uploads
- Separate media server
- CDN for static assets

---

## Performance Optimizations

### Current Optimizations
1. **Database**:
   - `select_related()` for foreign keys
   - `prefetch_related()` for many-to-many
   - Pagination (50 records per page)

2. **Templates**:
   - Minimal template logic
   - Cached template compilation
   - CDN for CSS/fonts

3. **Queries**:
   - Filtered at database level
   - Indexed fields (id, date, ep_no)
   - Bulk operations for CSV import

### Future Optimizations
- Query result caching
- Template fragment caching
- Lazy loading for images
- Minified CSS/JS
- Gzip compression
- Database query optimization

---

## Error Handling

### Levels
1. **Application Level**: Try-catch in views
2. **Service Level**: Business logic validation
3. **Database Level**: Model validation
4. **HTTP Level**: Custom error pages

### Error Pages
- **403**: Access denied
- **403_csrf**: CSRF failure (custom)
- **404**: Page not found
- **500**: Server error

### Logging
- File-based logging (`logs/`)
- Console output (development)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Separate loggers for Django and app

---

## Testing Strategy

### Test Types
1. **Unit Tests**: Service layer logic
2. **Integration Tests**: View + model interactions
3. **Property-Based Tests**: Request approval logic
4. **Manual Tests**: UI/UX on devices

### Test Coverage
- Service layer: High priority
- Views: Medium priority
- Models: Low priority (Django tested)
- Templates: Manual testing

---

## Deployment Architecture

### Development
```
Local Machine
    ↓
Django Dev Server (manage.py runserver)
    ↓
SQLite Database
    ↓
File-based logging
```

### Production (Recommended)
```
Load Balancer
    ↓
Nginx (Reverse Proxy)
    ↓
Gunicorn (WSGI Server)
    ↓
Django Application
    ↓
PostgreSQL Database
    ↓
Redis (Cache/Sessions)
    ↓
Centralized Logging
```

---

## API Design (Internal)

### URL Structure
```
/                          # Dashboard
/login/                    # Login page
/logout/                   # Logout action
/upload/                   # CSV upload
/attendance/               # Attendance list
/attendance/<id>/edit/     # Edit record
/attendance/<id>/delete/   # Delete record
/users/                    # User management
/users/create/             # Create user
/users/<id>/edit/          # Edit user
/admin/requests/           # Access requests
/admin/assignments/        # Manage assignments
```

### View Patterns
- List views: Paginated, filtered
- Detail views: Single object
- Create views: Form + POST
- Update views: Form + POST
- Delete views: Confirmation + POST

---

## Configuration Management

### Settings Structure
```python
# Base settings
DEBUG = True/False
ALLOWED_HOSTS = []
SECRET_KEY = '...'

# Database
DATABASES = {...}

# Static files
STATIC_URL = '/static/'

# Custom
AUTH_USER_MODEL = 'core.User'
LOGIN_URL = '/login/'
CSRF_FAILURE_VIEW = 'core.views.csrf_failure'
```

### Environment-Specific
- Development: DEBUG=True, SQLite
- Staging: DEBUG=False, PostgreSQL
- Production: DEBUG=False, PostgreSQL, Redis

---

## Monitoring & Maintenance

### Logging
- Application logs: `logs/attendance_system.log`
- Django logs: Console + file
- Error tracking: File-based

### Metrics (Future)
- Request count
- Response times
- Error rates
- User activity
- Database performance

### Backup Strategy
- Database: Daily backups
- Files: Weekly backups
- Logs: Rotate weekly
- Retention: 30 days

---

## Technical Decisions

### Why Django?
- Rapid development
- Built-in admin
- ORM for database abstraction
- Security features
- Large ecosystem

### Why SQLite?
- Zero configuration
- File-based (portable)
- Sufficient for small-medium scale
- Easy backup

### Why TailwindCSS (CDN)?
- No build process
- Rapid prototyping
- Consistent design
- Small footprint

### Why No JavaScript Framework?
- Simple interactions
- Faster page loads
- Less complexity
- Progressive enhancement

---

**Last Updated:** November 28, 2025  
**Version:** 1.0.0
