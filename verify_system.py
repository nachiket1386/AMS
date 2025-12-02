#!/usr/bin/env python
"""
System Verification Script
Run this to verify the attendance system is properly set up
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from django.core.management import call_command
from core.models import User, Company, AttendanceRecord, UploadLog

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def verify_database():
    """Verify database is set up correctly"""
    print_header("Database Verification")
    
    try:
        # Check if tables exist
        User.objects.count()
        Company.objects.count()
        AttendanceRecord.objects.count()
        UploadLog.objects.count()
        print_success("All database tables exist")
        return True
    except Exception as e:
        print_error(f"Database error: {e}")
        print_info("Run: python manage.py migrate")
        return False

def verify_users():
    """Verify initial users exist"""
    print_header("User Verification")
    
    users_to_check = [
        ('root', 'root'),
        ('admin', 'admin'),
        ('user1', 'user1')
    ]
    
    all_exist = True
    for username, role in users_to_check:
        try:
            user = User.objects.get(username=username)
            print_success(f"User '{username}' exists (Role: {user.role})")
        except User.DoesNotExist:
            print_error(f"User '{username}' not found")
            all_exist = False
    
    if not all_exist:
        print_info("Run: python manage.py create_initial_data")
    
    return all_exist

def verify_companies():
    """Verify companies exist"""
    print_header("Company Verification")
    
    company_count = Company.objects.count()
    if company_count > 0:
        print_success(f"Found {company_count} companies")
        for company in Company.objects.all():
            print_info(f"  - {company.name}")
        return True
    else:
        print_error("No companies found")
        print_info("Run: python manage.py create_initial_data")
        return False

def verify_files():
    """Verify required files exist"""
    print_header("File Verification")
    
    required_files = [
        'manage.py',
        'attendance_system/settings.py',
        'core/models.py',
        'core/views.py',
        'core/forms.py',
        'core/csv_processor.py',
        'core/templates/base.html',
        'core/templates/login.html',
        'sample_attendance.csv',
        'README.md',
        'QUICKSTART.md'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} not found")
            all_exist = False
    
    return all_exist

def verify_tests():
    """Run tests"""
    print_header("Running Tests")
    
    try:
        print_info("Running test suite...")
        result = call_command('test', '--verbosity=0')
        print_success("All tests passed!")
        return True
    except Exception as e:
        print_error(f"Tests failed: {e}")
        return False

def verify_system_check():
    """Run Django system check"""
    print_header("System Check")
    
    try:
        call_command('check')
        print_success("System check passed")
        return True
    except Exception as e:
        print_error(f"System check failed: {e}")
        return False

def print_summary(results):
    """Print verification summary"""
    print_header("Verification Summary")
    
    total = len(results)
    passed = sum(results.values())
    
    for check, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print_success("\n🎉 System is ready to use!")
        print_info("\nQuick Start:")
        print_info("  1. python manage.py runserver")
        print_info("  2. Open http://127.0.0.1:8000")
        print_info("  3. Login with root/root123")
    else:
        print_error("\n⚠️  Some checks failed. Please fix the issues above.")

def main():
    """Main verification function"""
    print_header("Attendance Management System - Verification")
    print_info("Checking system setup...\n")
    
    results = {
        'Database': verify_database(),
        'Users': verify_users(),
        'Companies': verify_companies(),
        'Files': verify_files(),
        'System Check': verify_system_check(),
        'Tests': verify_tests(),
    }
    
    print_summary(results)

if __name__ == '__main__':
    main()
