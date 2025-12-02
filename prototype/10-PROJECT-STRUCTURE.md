# Project Structure

This document explains the complete project structure and what each folder contains.

---

## 📦 Root Directory Overview

```
attendance-system/
├── 📁 attendance-management-system (1)/  ⚠️ SEPARATE FRONTEND APP (DO NOT MODIFY)
├── 📁 attendance_system/                 Django project settings
├── 📁 core/                              Main Django application
├── 📁 docs/                              📚 All documentation (ORGANIZED)
├── 📁 .kiro/                             Kiro IDE specs and settings
├── 📁 logs/                              Application logs
├── 📁 .hypothesis/                       Property-based testing data
├── 📁 .pytest_cache/                     Pytest cache
├── 📁 .vscode/                           VS Code settings
├── 📄 manage.py                          Django management script
├── 📄 db.sqlite3                         SQLite database
├── 📄 requirements.txt                   Python dependencies
├── 📄 README.md                          Main project README
├── 📄 DOCUMENTATION_STRUCTURE.md         Documentation organization guide
└── 📄 docker-compose.yml                 Docker configuration
```

---

## 🎯 Key Folders Explained

### 1. `attendance-management-system (1)/` ⚠️ IMPORTANT

**Type:** React/TypeScript Frontend Application  
**Purpose:** Separate frontend instance (possibly for testing or alternative UI)  
**Status:** ⚠️ **DO NOT MODIFY** - This is used to run your application

**Contents:**
- React components
- TypeScript files
- Vite configuration
- Package.json (Node.js dependencies)

**Technology Stack:**
- React
- TypeScript
- Vite (build tool)

**Note:** This is a **separate application** from the main Django backend. It's not part of the Django project structure.

---

### 2. `attendance_system/` - Django Project

**Type:** Django Project Configuration  
**Purpose:** Main Django project settings and configuration

**Key Files:**
- `settings.py` - Django settings
- `urls.py` - Root URL configuration
- `wsgi.py` - WSGI configuration for deployment
- `asgi.py` - ASGI configuration

---

### 3. `core/` - Main Django Application

**Type:** Django Application  
**Purpose:** Core attendance management functionality

**Structure:**
```
core/
├── migrations/              Database migrations
├── services/               Business logic services
│   ├── access_control_service.py
│   └── request_approval_service.py
├── templates/              HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── attendance_list.html
│   ├── request_access.html
│   ├── my_requests.html
│   ├── approve_requests.html
│   └── manage_assignments.html
├── templatetags/           Custom template filters
├── tests/                  Test files
│   ├── test_access_control_service.py
│   ├── test_request_approval_service.py
│   ├── test_property_request_approval.py
│   └── test_property_bulk_request.py
├── models.py              Database models
├── views.py               View functions
├── urls.py                URL routing
├── forms.py               Django forms
└── admin.py               Admin interface
```

---

### 4. `docs/` - Documentation 📚

**Type:** Organized Documentation  
**Purpose:** All project documentation in one place

**Structure:**
```
docs/
├── README.md                          Documentation index
├── deployment/
│   └── DEPLOYMENT_GUIDE.md           Complete deployment guide
├── design/
│   ├── DESIGN_COMPLIANCE.md          Design system
│   ├── FRONTEND_DESIGN_SYSTEM.md     Frontend guidelines
│   └── DESIGN_NOTES.md               Additional notes
├── features/
│   ├── USER1_SUPERVISOR_MANAGEMENT.md
│   ├── NAVIGATION_REDESIGN.md
│   └── COMPLETE_IMPLEMENTATION.md
├── guides/
│   ├── QUICKSTART.md
│   ├── UPLOAD_INSTRUCTIONS.md
│   └── A-Z.md
└── project/
    ├── PROJECT_SUMMARY.md
    ├── STATUS.md
    └── README.md
```

---

### 5. `.kiro/` - Kiro IDE Configuration

**Type:** IDE Configuration  
**Purpose:** Kiro IDE specs and settings

**Structure:**
```
.kiro/
├── specs/
│   └── user1-supervisor-management/
│       ├── requirements.md           Feature requirements
│       ├── design.md                 Feature design
│       └── tasks.md                  Implementation tasks
└── settings/
    └── (IDE settings)
```

---

### 6. `logs/` - Application Logs

**Type:** Log Files  
**Purpose:** Application logging and debugging

**Contents:**
- Django application logs
- Error logs
- Access logs

---

## 🔍 Important Files

### Root Level Files

| File | Purpose |
|------|---------|
| `manage.py` | Django management commands |
| `db.sqlite3` | SQLite database (development) |
| `requirements.txt` | Python dependencies |
| `README.md` | Main project README |
| `DOCUMENTATION_STRUCTURE.md` | Documentation organization |
| `PROJECT_STRUCTURE.md` | This file |
| `docker-compose.yml` | Docker configuration |
| `Dockerfile` | Docker image definition |
| `nginx.conf` | Nginx configuration |
| `pytest.ini` | Pytest configuration |

---

## 🚀 Running the Applications

### Django Backend (Main Application)

```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Run Django server
python manage.py runserver
```

**Access:** http://127.0.0.1:8000

---

### React Frontend (attendance-management-system (1)/)

```bash
# Navigate to frontend folder
cd "attendance-management-system (1)"

# Install dependencies (first time only)
npm install

# Run development server
npm run dev
```

**Access:** http://localhost:5173 (or port shown in terminal)

---

## 📊 Project Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                        │
│  attendance-management-system (1)/                       │
│  (React + TypeScript + Vite)                            │
└─────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/API
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Backend Layer                         │
│  Django Application (attendance_system/ + core/)         │
│  - Views & Templates                                     │
│  - Business Logic (Services)                             │
│  - Database Models                                       │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Database Layer                        │
│  SQLite (Development) / PostgreSQL (Production)          │
└─────────────────────────────────────────────────────────┘
```

---

## ⚠️ Important Notes

### DO NOT MODIFY
- `attendance-management-system (1)/` - Separate frontend app
- `.hypothesis/` - Auto-generated testing data
- `.pytest_cache/` - Auto-generated pytest cache
- `__pycache__/` - Python bytecode cache

### SAFE TO MODIFY
- `core/` - Main application code
- `attendance_system/settings.py` - Configuration
- `docs/` - Documentation
- `requirements.txt` - Dependencies

### GENERATED FILES
- `db.sqlite3` - Database (can be regenerated)
- `logs/` - Log files (can be cleared)
- `staticfiles/` - Collected static files (regenerated)

---

## 🔄 Relationship Between Folders

### Django Backend (Main Project)
```
attendance_system/ + core/ + manage.py
↓
Handles all backend logic, database, authentication, business rules
```

### React Frontend (Separate)
```
attendance-management-system (1)/
↓
Provides alternative UI (possibly for testing or specific use case)
```

### Documentation
```
docs/
↓
Documents both backend and frontend
```

---

## 📝 Development Workflow

### Working on Backend (Django)
1. Activate virtual environment
2. Make changes in `core/` or `attendance_system/`
3. Run migrations if models changed
4. Test with `python manage.py test`
5. Run server with `python manage.py runserver`

### Working on Frontend (React)
1. Navigate to `attendance-management-system (1)/`
2. Make changes in components or pages
3. Test with `npm run dev`
4. Build with `npm run build`

### Working on Documentation
1. Navigate to `docs/`
2. Edit relevant .md files
3. Update `docs/README.md` if adding new docs

---

## 🎯 Quick Reference

**Run Django backend:**
```bash
python manage.py runserver
```

**Run React frontend:**
```bash
cd "attendance-management-system (1)"
npm run dev
```

**Run tests:**
```bash
python manage.py test
pytest
```

**View documentation:**
```bash
# Open docs/README.md in browser or editor
```

**Deploy application:**
```bash
# See docs/deployment/DEPLOYMENT_GUIDE.md
```

---

## 📞 Support

- **Django Backend Issues:** Check `logs/` folder and Django documentation
- **React Frontend Issues:** Check browser console and React documentation
- **Documentation:** Start with `docs/README.md`
- **Deployment:** See `docs/deployment/DEPLOYMENT_GUIDE.md`

---

**Project Structure Version:** 1.0.0  
**Last Updated:** November 2025  
**Status:** ✅ Documented and Organized
