"""
Fix existing manday records to use correct company from attendance records
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import AttendanceRecord, MandaySummaryRecord
from django.db.models import Count

print("="*70)
print("FIXING MANDAY COMPANY ASSIGNMENTS")
print("="*70)

# Get all unique employee numbers from manday records
all_ep_nos = MandaySummaryRecord.objects.values_list('ep_no', flat=True).distinct()
print(f"\nFound {len(all_ep_nos)} unique employees in manday records")

fixed_count = 0
no_attendance_count = 0
already_correct_count = 0
error_count = 0

print("\nProcessing employees...")
print("-"*70)

for ep_no in all_ep_nos:
    # Get the employee's correct company from attendance records
    attendance = AttendanceRecord.objects.filter(ep_no=ep_no).first()
    
    if not attendance:
        no_attendance_count += 1
        print(f"⚠ {ep_no}: No attendance records found - skipping")
        continue
    
    correct_company = attendance.company
    
    # Get all manday records for this employee
    manday_records = MandaySummaryRecord.objects.filter(ep_no=ep_no)
    
    # Check if any have wrong company
    wrong_company_records = manday_records.exclude(company=correct_company)
    
    if wrong_company_records.exists():
        wrong_count = wrong_company_records.count()
        old_companies = wrong_company_records.values_list('company__name', flat=True).distinct()
        
        try:
            # Update all wrong records to correct company
            updated = wrong_company_records.update(company=correct_company)
            fixed_count += updated
            print(f"✓ {ep_no}: Fixed {updated} records")
            print(f"  From: {', '.join(set(old_companies))}")
            print(f"  To: {correct_company.name}")
        except Exception as e:
            error_count += 1
            print(f"✗ {ep_no}: Error - {str(e)}")
    else:
        already_correct_count += 1

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Total employees processed: {len(all_ep_nos)}")
print(f"✓ Records fixed: {fixed_count}")
print(f"✓ Already correct: {already_correct_count}")
print(f"⚠ No attendance data: {no_attendance_count}")
print(f"✗ Errors: {error_count}")
print("\n✓ Fix complete!")
