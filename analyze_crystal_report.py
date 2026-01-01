"""
Complete analysis of CrystalReportViewer1.xlsx
"""
import win32com.client
import os

excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

filepath = os.path.abspath('CrystalReportViewer1.xlsx')
workbook = excel.Workbooks.Open(filepath)

print("=" * 100)
print("CRYSTAL REPORT VIEWER - COMPLETE ANALYSIS")
print("=" * 100)

sheet = workbook.Sheets(1)
rows = sheet.UsedRange.Rows.Count
cols = sheet.UsedRange.Columns.Count

print(f"\n📊 Sheet Name: {sheet.Name}")
print(f"📏 Dimensions: {rows} rows × {cols} columns")
print(f"📍 Used Range: {sheet.UsedRange.Address}")

# Get all headers from row 1 and row 2
print("\n" + "=" * 100)
print("COLUMN STRUCTURE")
print("=" * 100)

headers_row1 = []
headers_row2 = []

for col in range(1, min(cols + 1, 50)):  # First 50 columns
    val1 = sheet.Cells(1, col).Value
    val2 = sheet.Cells(2, col).Value
    headers_row1.append(val1 if val1 else "")
    headers_row2.append(val2 if val2 else "")

print("\nFirst 30 Columns:")
for i in range(min(30, len(headers_row1))):
    row1_val = headers_row1[i] if headers_row1[i] else "(empty)"
    row2_val = headers_row2[i] if headers_row2[i] else "(empty)"
    print(f"  Col {i+1:2d}: Row1='{row1_val}' | Row2='{row2_val}'")

# Analyze data structure
print("\n" + "=" * 100)
print("DATA ANALYSIS")
print("=" * 100)

# Get sample employee records
print("\nSample Employee Records (First 10):")
print("-" * 100)

for row in range(5, min(15, rows + 1)):  # Rows 5-14 (assuming data starts at row 5)
    ep_no = sheet.Cells(row, 1).Value
    ep_name = sheet.Cells(row, 2).Value
    cont_code = sheet.Cells(row, 3).Value
    contractor = sheet.Cells(row, 4).Value
    sector = sheet.Cells(row, 5).Value
    area = sheet.Cells(row, 6).Value
    plant = sheet.Cells(row, 7).Value
    dept = sheet.Cells(row, 8).Value
    eic = sheet.Cells(row, 9).Value
    trade = sheet.Cells(row, 10).Value
    skill = sheet.Cells(row, 11).Value
    card_cat = sheet.Cells(row, 12).Value
    
    if ep_no:
        print(f"\nEmployee {row-4}:")
        print(f"  EP NO: {ep_no}")
        print(f"  Name: {ep_name}")
        print(f"  Contractor Code: {cont_code}")
        print(f"  Contractor: {contractor}")
        print(f"  Sector: {sector}")
        print(f"  Area: {area}")
        print(f"  Plant: {plant}")
        print(f"  Department: {dept}")
        print(f"  EIC: {eic}")
        print(f"  Trade: {trade}")
        print(f"  Skill: {skill}")
        print(f"  Card Category: {card_cat}")

# Count total employees
print("\n" + "=" * 100)
print("STATISTICS")
print("=" * 100)

employee_count = 0
for row in range(5, rows + 1):
    ep_no = sheet.Cells(row, 1).Value
    if ep_no and str(ep_no).startswith('PP'):
        employee_count += 1

print(f"\n📊 Total Employees: {employee_count}")
print(f"📅 Report Period: {sheet.Cells(1, 1).Value} {sheet.Cells(1, 2).Value}")

# Identify date columns
print("\n📅 Date Columns Detected:")
date_cols = []
for col in range(13, min(cols + 1, 50)):
    val = sheet.Cells(2, col).Value
    if val and ('/' in str(val) or '2025' in str(val)):
        date_cols.append((col, val))
        if len(date_cols) <= 10:
            print(f"  Column {col}: {val}")

if len(date_cols) > 10:
    print(f"  ... and {len(date_cols) - 10} more date columns")

print(f"\n📆 Total Date Columns: {len(date_cols)}")

# Sample attendance data
print("\n" + "=" * 100)
print("SAMPLE ATTENDANCE DATA")
print("=" * 100)

if employee_count > 0:
    # Get first employee's attendance for first 5 dates
    print(f"\nFirst Employee Attendance (First 5 Days):")
    ep_no = sheet.Cells(5, 1).Value
    ep_name = sheet.Cells(5, 2).Value
    print(f"Employee: {ep_no} - {ep_name}")
    
    for i, (col, date) in enumerate(date_cols[:5]):
        shift = sheet.Cells(5, col).Value
        plant_in = sheet.Cells(5, col + 1).Value if col + 1 <= cols else None
        plant_out = sheet.Cells(5, col + 2).Value if col + 2 <= cols else None
        status = sheet.Cells(5, col + 3).Value if col + 3 <= cols else None
        
        print(f"\n  Date: {date}")
        print(f"    Shift: {shift}")
        print(f"    Plant In: {plant_in}")
        print(f"    Plant Out: {plant_out}")
        print(f"    Status: {status}")

print("\n" + "=" * 100)
print("REPORT SUMMARY")
print("=" * 100)
print(f"""
This appears to be a MONTHLY ATTENDANCE REPORT with:
- {employee_count} employees
- {len(date_cols)} days of attendance data
- Employee details (EP NO, Name, Contractor, Department, etc.)
- Daily attendance (Shift, Plant In/Out times, Status)
- Report period: {sheet.Cells(1, 1).Value} {sheet.Cells(1, 2).Value}
""")

workbook.Close(False)
excel.Quit()

print("=" * 100)
