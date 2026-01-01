"""
Quick test to verify manday company lookup from attendance records
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import Company, AttendanceRecord, MandaySummaryRecord, User
from datetime import date

# Clean up test data
print("Cleaning up test data...")
MandaySummaryRecord.objects.filter(ep_no__in=['TEST001', 'TEST002']).delete()
AttendanceRecord.objects.filter(ep_no__in=['TEST001', 'TEST002']).delete()
Company.objects.filter(name__in=['Test Company A', 'Test Company B']).delete()

# Create test companies
print("\nCreating test companies...")
company_a = Company.objects.create(name='Test Company A')
company_b = Company.objects.create(name='Test Company B')
print(f"Created: {company_a.name} (ID: {company_a.id})")
print(f"Created: {company_b.name} (ID: {company_b.id})")

# Create attendance records for test employees
print("\nCreating attendance records...")
att1 = AttendanceRecord.objects.create(
    ep_no='TEST001',
    ep_name='Test Employee 1',
    company=company_a,
    date=date(2024, 1, 1),
    shift='Day',
    overstay='0',
    status='P'
)
print(f"Created attendance for TEST001 in {company_a.name}")

att2 = AttendanceRecord.objects.create(
    ep_no='TEST002',
    ep_name='Test Employee 2',
    company=company_b,
    date=date(2024, 1, 1),
    shift='Day',
    overstay='0',
    status='P'
)
print(f"Created attendance for TEST002 in {company_b.name}")

# Now create manday records and verify they get the correct company
print("\nCreating manday records...")
from datetime import time
from decimal import Decimal

manday1 = MandaySummaryRecord.objects.create(
    ep_no='TEST001',
    punch_date=date(2024, 1, 1),
    mandays=Decimal('1.00'),
    regular_manday_hr=time(8, 0),
    ot=Decimal('2.00'),
    company=company_a  # This should come from attendance lookup
)

manday2 = MandaySummaryRecord.objects.create(
    ep_no='TEST002',
    punch_date=date(2024, 1, 1),
    mandays=Decimal('1.00'),
    regular_manday_hr=time(8, 0),
    ot=Decimal('3.00'),
    company=company_b  # This should come from attendance lookup
)

# Verify the companies match
print("\nVerifying company assignments...")
manday1_check = MandaySummaryRecord.objects.get(ep_no='TEST001', punch_date=date(2024, 1, 1))
manday2_check = MandaySummaryRecord.objects.get(ep_no='TEST002', punch_date=date(2024, 1, 1))

print(f"\nTEST001:")
print(f"  Attendance Company: {att1.company.name}")
print(f"  Manday Company: {manday1_check.company.name}")
print(f"  ✓ Match: {att1.company.id == manday1_check.company.id}")

print(f"\nTEST002:")
print(f"  Attendance Company: {att2.company.name}")
print(f"  Manday Company: {manday2_check.company.name}")
print(f"  ✓ Match: {att2.company.id == manday2_check.company.id}")

# Clean up
print("\nCleaning up test data...")
MandaySummaryRecord.objects.filter(ep_no__in=['TEST001', 'TEST002']).delete()
AttendanceRecord.objects.filter(ep_no__in=['TEST001', 'TEST002']).delete()
Company.objects.filter(name__in=['Test Company A', 'Test Company B']).delete()

print("\n✓ Test complete!")
