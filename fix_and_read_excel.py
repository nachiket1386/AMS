"""
Try multiple methods to read the corrupted Excel file
"""
import sys

print("=" * 80)
print("ATTEMPTING TO READ: CrystalReportViewer1.xlsx")
print("=" * 80)

# Method 1: Try with xlrd (for older Excel formats)
print("\n[Method 1] Trying xlrd...")
try:
    import xlrd
    workbook = xlrd.open_workbook('CrystalReportViewer1.xlsx', ignore_workbook_corruption=True)
    print(f"✅ Success with xlrd!")
    print(f"Sheets: {workbook.sheet_names()}")
    
    for sheet_name in workbook.sheet_names():
        sheet = workbook.sheet_by_name(sheet_name)
        print(f"\n📊 Sheet: {sheet_name}")
        print(f"Rows: {sheet.nrows}, Columns: {sheet.ncols}")
        
        # Print headers
        if sheet.nrows > 0:
            print("\nHeaders:")
            for col in range(sheet.ncols):
                print(f"  {col+1}. {sheet.cell_value(0, col)}")
        
        # Print first 5 data rows
        print("\nFirst 5 rows:")
        for row in range(min(6, sheet.nrows)):
            print(f"\nRow {row+1}:")
            for col in range(sheet.ncols):
                val = sheet.cell_value(row, col)
                if val:
                    print(f"  Col {col+1}: {val}")
    
    sys.exit(0)
except Exception as e:
    print(f"❌ Failed: {e}")

# Method 2: Try converting with win32com (Windows only)
print("\n[Method 2] Trying win32com (Windows Excel COM)...")
try:
    import win32com.client
    import os
    
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    
    filepath = os.path.abspath('CrystalReportViewer1.xlsx')
    workbook = excel.Workbooks.Open(filepath)
    
    print(f"✅ Success with win32com!")
    print(f"Sheets: {workbook.Sheets.Count}")
    
    for i in range(1, workbook.Sheets.Count + 1):
        sheet = workbook.Sheets(i)
        print(f"\n📊 Sheet: {sheet.Name}")
        print(f"Used Range: {sheet.UsedRange.Address}")
        
        # Get dimensions
        rows = sheet.UsedRange.Rows.Count
        cols = sheet.UsedRange.Columns.Count
        print(f"Rows: {rows}, Columns: {cols}")
        
        # Print headers
        print("\nHeaders:")
        for col in range(1, min(cols + 1, 20)):
            val = sheet.Cells(1, col).Value
            if val:
                print(f"  {col}. {val}")
        
        # Print first 5 data rows
        print("\nFirst 5 data rows:")
        for row in range(2, min(7, rows + 1)):
            print(f"\nRow {row}:")
            for col in range(1, min(cols + 1, 20)):
                val = sheet.Cells(row, col).Value
                if val:
                    header = sheet.Cells(1, col).Value
                    print(f"  {header}: {val}")
    
    workbook.Close(False)
    excel.Quit()
    
    sys.exit(0)
except Exception as e:
    print(f"❌ Failed: {e}")

# Method 3: Try pyxlsb for binary Excel files
print("\n[Method 3] Trying pyxlsb...")
try:
    from pyxlsb import open_workbook
    
    with open_workbook('CrystalReportViewer1.xlsx') as wb:
        print(f"✅ Success with pyxlsb!")
        print(f"Sheets: {wb.sheets}")
        
        for sheet_name in wb.sheets:
            with wb.get_sheet(sheet_name) as sheet:
                print(f"\n📊 Sheet: {sheet_name}")
                
                rows = list(sheet.rows())
                print(f"Total rows: {len(rows)}")
                
                if rows:
                    # Print headers
                    print("\nHeaders:")
                    for i, cell in enumerate(rows[0], 1):
                        if cell.v:
                            print(f"  {i}. {cell.v}")
                    
                    # Print first 5 data rows
                    print("\nFirst 5 data rows:")
                    for row_idx, row in enumerate(rows[1:6], 2):
                        print(f"\nRow {row_idx}:")
                        for col_idx, cell in enumerate(row, 1):
                            if cell.v:
                                header = rows[0][col_idx-1].v if col_idx-1 < len(rows[0]) else f"Col{col_idx}"
                                print(f"  {header}: {cell.v}")
    
    sys.exit(0)
except Exception as e:
    print(f"❌ Failed: {e}")

print("\n" + "=" * 80)
print("❌ ALL METHODS FAILED")
print("=" * 80)
print("\nThe Excel file appears to be corrupted.")
print("Please try:")
print("1. Open the file in Excel and save it as a new file")
print("2. Or save it as CSV format")
print("3. Or copy the data and paste into a new Excel file")
