"""
Check employee 101075428's company assignment
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import AttendanceRecord, MandaySummaryRecord

ep_no = '101075428'

print(f"Checking employee: {ep_no}\n")

# Check attendance records
print("=== ATTENDANCE RECORDS ===")
attendance_records = AttendanceRecord.objects.filter(ep_no=ep_no)
if attendance_records.exists():
    for record in attendance_records[:5]:  # Show first 5
        print(f"Date: {record.date}, Company: {record.company.name}, Name: {record.ep_name}")
    print(f"Total attendance records: {attendance_records.count()}")
    
    # Get the company from first record
    first_record = attendance_records.first()
    correct_company = first_record.company
    print(f"\n✓ Employee's correct company: {correct_company.name}")
else:
    print(f"No attendance records found for {ep_no}")
    correct_company = None

# Check manday records
print(f"\n=== MANDAY RECORDS ===")
manday_records = MandaySummaryRecord.objects.filter(ep_no=ep_no)
if manday_records.exists():
    for record in manday_records[:5]:  # Show first 5
        print(f"Date: {record.punch_date}, Company: {record.company.name}, Mandays: {record.mandays}, OT: {record.ot}")
    print(f"Total manday records: {manday_records.count()}")
    
    # Check if all manday records have the correct company
    if correct_company:
        wrong_company_count = manday_records.exclude(company=correct_company).count()
        if wrong_company_count > 0:
            print(f"\n⚠ WARNING: {wrong_company_count} manday records have WRONG company!")
            print("\nRecords with wrong company:")
            for record in manday_records.exclude(company=correct_company)[:10]:
                print(f"  Date: {record.punch_date}, Wrong Company: {record.company.name}")
        else:
            print(f"\n✓ All manday records have correct company: {correct_company.name}")
else:
    print(f"No manday records found for {ep_no}")

print("\n" + "="*50)
print("RECOMMENDATION:")
if correct_company and manday_records.exists():
    wrong_count = manday_records.exclude(company=correct_company).count()
    if wrong_count > 0:
        print(f"You need to update {wrong_count} manday records to use company: {correct_company.name}")
        print("\nTo fix existing records, you can:")
        print("1. Delete the wrong manday records")
        print("2. Re-upload the manday CSV file")
        print("3. The new upload will use the correct company from attendance records")
    else:
        print("All records are correct! No action needed.")
else:
    print("Upload attendance data first, then upload manday data.")
