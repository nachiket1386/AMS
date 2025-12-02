# Quick Reference Guide

Fast access to everything you need.

---

## 🚀 Quick Start

### Run Django Backend
```bash
python manage.py runserver
```
Access: http://127.0.0.1:8000

### Run React Frontend
```bash
cd "attendance-management-system (1)"
npm run dev
```
Access: http://localhost:5173

---

## 📁 Where Is Everything?

| What You Need | Location |
|---------------|----------|
| **Documentation** | `docs/README.md` |
| **Deployment Guide** | `docs/deployment/DEPLOYMENT_GUIDE.md` |
| **Quick Start** | `docs/guides/QUICKSTART.md` |
| **Project Structure** | `PROJECT_STRUCTURE.md` |
| **Django Code** | `core/` folder |
| **React Frontend** | `attendance-management-system (1)/` |
| **Database** | `db.sqlite3` |
| **Settings** | `attendance_system/settings.py` |
| **Tests** | `core/tests/` |
| **Logs** | `logs/` folder |

---

## 📚 Documentation Quick Links

### Getting Started
- [Quick Start Guide](docs/guides/QUICKSTART.md)
- [Upload Instructions](docs/guides/UPLOAD_INSTRUCTIONS.md)
- [A-Z Features](docs/guides/A-Z.md)

### Deployment
- [Complete Deployment Guide](docs/deployment/DEPLOYMENT_GUIDE.md)
  - Local Development
  - PythonAnywhere (Easiest)
  - Oracle Cloud (Free)
  - Docker

### Features
- [User1 Supervisor Management](docs/features/USER1_SUPERVISOR_MANAGEMENT.md)
- [Navigation Redesign](docs/features/NAVIGATION_REDESIGN.md)
- [Complete Implementation](docs/features/COMPLETE_IMPLEMENTATION.md)

### Design
- [Design Compliance](docs/design/DESIGN_COMPLIANCE.md)
- [Frontend Design System](docs/design/FRONTEND_DESIGN_SYSTEM.md)

### Project Info
- [Project Summary](docs/project/PROJECT_SUMMARY.md)
- [Current Status](docs/project/STATUS.md)

---

## 🔧 Common Commands

### Django Commands
```bash
# Run server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell
```

### React Commands
```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Testing Commands
```bash
# Run all tests
pytest

# Run specific test file
pytest core/tests/test_access_control_service.py

# Run with coverage
pytest --cov=core

# Run property-based tests
pytest core/tests/test_property_*.py
```

---

## 🎯 Project Structure at a Glance

```
📦 Root
├── 📁 attendance-management-system (1)/  ⚠️ React Frontend (DO NOT MODIFY)
├── 📁 attendance_system/                 Django settings
├── 📁 core/                              Main Django app
├── 📁 docs/                              📚 All documentation
│   ├── deployment/
│   ├── design/
│   ├── features/
│   ├── guides/
│   └── project/
├── 📁 .kiro/                             Kiro specs
├── 📁 logs/                              Application logs
├── 📄 manage.py                          Django CLI
├── 📄 db.sqlite3                         Database
└── 📄 requirements.txt                   Dependencies
```

---

## 🔐 Default Login Credentials

### Root User (Full Access)
- Username: `root`
- Password: `root123`

### Admin User (Company Admin)
- Username: `admin`
- Password: `admin123`

### User1 (Supervisor)
- Username: `user1`
- Password: `user123`

⚠️ **Change these in production!**

---

## 🆘 Troubleshooting

### Django Issues

**Can't start server?**
```bash
python manage.py check
python manage.py migrate
```

**Database errors?**
```bash
python manage.py migrate
python manage.py makemigrations
```

**Static files not loading?**
```bash
python manage.py collectstatic --noinput
```

### React Issues

**Dependencies error?**
```bash
cd "attendance-management-system (1)"
rm -rf node_modules package-lock.json
npm install
```

**Port already in use?**
```bash
# Kill process on port 5173
# Windows: netstat -ano | findstr :5173
# Mac/Linux: lsof -ti:5173 | xargs kill
```

---

## 📊 Key Features

### For All Users
- ✅ Dashboard with statistics
- ✅ View attendance records
- ✅ Search and filter
- ✅ Export to CSV

### For User1 (Supervisors)
- ✅ View assigned employees only
- ✅ Request access to employees
- ✅ Track request status
- ✅ Overstay highlighting

### For Admins
- ✅ Approve/reject access requests
- ✅ Manage employee assignments
- ✅ Upload CSV data
- ✅ User management
- ✅ Audit logs

### For Root
- ✅ Full system access
- ✅ All admin features
- ✅ System configuration
- ✅ Backup/restore

---

## 🌐 URLs

### Django Backend
- Dashboard: `/`
- Login: `/login/`
- Attendance: `/attendance/`
- Upload: `/upload/`
- Users: `/users/`
- Request Access: `/request-access/`
- My Requests: `/my-requests/`
- Approve Requests: `/approve-requests/`
- Manage Assignments: `/manage-assignments/`

### React Frontend
- Home: `/`
- (Check `attendance-management-system (1)/` for routes)

---

## 💡 Tips

1. **Always activate virtual environment** before running Django commands
2. **Check logs** in `logs/` folder for errors
3. **Run tests** before deploying
4. **Backup database** before major changes
5. **Read documentation** in `docs/` folder
6. **Don't modify** `attendance-management-system (1)/` folder

---

## 📞 Need Help?

1. Check `docs/README.md` for documentation index
2. Review `PROJECT_STRUCTURE.md` for project layout
3. See `docs/deployment/DEPLOYMENT_GUIDE.md` for deployment
4. Check `logs/` folder for error messages
5. Run `python manage.py check` for Django issues

---

**Quick Reference Version:** 1.0.0  
**Last Updated:** November 2025
