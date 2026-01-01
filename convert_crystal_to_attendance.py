"""
Convert CrystalReportViewer1.xlsx to attendance format for database upload
Extracts: EP NO, EP NAME, Date, SHIFT, Plant In, Plant Out, Status
"""
import win32com.client
import os
import csv
from datetime import datetime

print("=" * 100)
print("CONVERTING CRYSTAL REPORT TO ATTENDANCE FORMAT")
print("=" * 100)

# Open Excel file
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

filepath = os.path.abspath('CrystalReportViewer1.xlsx')
workbook = excel.Workbooks.Open(filepath)
sheet = workbook.Sheets(1)

rows = sheet.UsedRange.Rows.Count
cols = sheet.UsedRange.Columns.Count

print(f"\n📊 Source: {rows} rows × {cols} columns")

# Identify date columns (starting from column 13)
date_columns = []
print("\n📅 Detecting date columns...")

for col in range(13, cols + 1, 4):  # Every 4 columns is a new date
    date_val = sheet.Cells(2, col).Value
    if date_val and '/' in str(date_val):
        # Parse date
        try:
            date_str = str(date_val)
            # Convert DD/MM/YYYY to YYYY-MM-DD
            parts = date_str.split('/')
            if len(parts) == 3:
                day, month, year = parts
                formatted_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                date_columns.append({
                    'date': formatted_date,
                    'date_display': date_str,
                    'shift_col': col,
                    'plant_in_col': col + 1,
                    'plant_out_col': col + 2,
                    'status_col': col + 3
                })
                print(f"  ✓ Found: {date_str} → {formatted_date} (Columns {col}-{col+3})")
        except Exception as e:
            print(f"  ✗ Error parsing date at column {col}: {e}")

print(f"\n📆 Total dates found: {len(date_columns)}")

# Extract attendance data
attendance_records = []
employee_count = 0

print("\n📋 Extracting attendance records...")

for row in range(5, rows + 1):  # Data starts at row 5
    ep_no = sheet.Cells(row, 1).Value
    ep_name = sheet.Cells(row, 2).Value
    
    # Skip if no EP NO
    if not ep_no or not str(ep_no).startswith('PP'):
        continue
    
    employee_count += 1
    
    # Extract attendance for each date
    for date_info in date_columns:
        shift = sheet.Cells(row, date_info['shift_col']).Value
        plant_in = sheet.Cells(row, date_info['plant_in_col']).Value
        plant_out = sheet.Cells(row, date_info['plant_out_col']).Value
        status = sheet.Cells(row, date_info['status_col']).Value
        
        # Only add record if there's some attendance data
        if shift or plant_in or plant_out or status:
            record = {
                'EP NO': str(ep_no).strip() if ep_no else '',
                'EP NAME': str(ep_name).strip() if ep_name else '',
                'DATE': date_info['date'],
                'SHIFT': str(shift).strip() if shift else '',
                'PLANT IN': str(plant_in).strip() if plant_in else '',
                'PLANT OUT': str(plant_out).strip() if plant_out else '',
                'STATUS': str(status).strip() if status else ''
            }
            attendance_records.append(record)

workbook.Close(False)
excel.Quit()

print(f"\n✅ Extracted {len(attendance_records)} attendance records from {employee_count} employees")

# Save to CSV
output_file = 'crystal_report_converted.csv'
print(f"\n💾 Saving to: {output_file}")

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['EP NO', 'EP NAME', 'DATE', 'SHIFT', 'PLANT IN', 'PLANT OUT', 'STATUS']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for record in attendance_records:
        writer.writerow(record)

print(f"✅ CSV file created successfully!")

# Show sample records
print("\n" + "=" * 100)
print("SAMPLE CONVERTED RECORDS (First 10)")
print("=" * 100)

for i, record in enumerate(attendance_records[:10], 1):
    print(f"\nRecord {i}:")
    for key, value in record.items():
        print(f"  {key}: {value}")

# Statistics
print("\n" + "=" * 100)
print("CONVERSION STATISTICS")
print("=" * 100)

print(f"""
📊 Total Employees: {employee_count}
📅 Total Dates: {len(date_columns)}
📋 Total Records: {len(attendance_records)}
💾 Output File: {output_file}

Date Range:
  From: {date_columns[0]['date_display']} ({date_columns[0]['date']})
  To: {date_columns[-1]['date_display']} ({date_columns[-1]['date']})
""")

print("=" * 100)
print("✅ CONVERSION COMPLETE!")
print("=" * 100)
print(f"\nNext step: Upload '{output_file}' to your Django application")
print("The file is ready for import into your attendance management system.")
