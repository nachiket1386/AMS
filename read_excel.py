import pandas as pd
import sys

try:
    # Read the Excel file
    excel_file = 'CrystalReportViewer1.xlsx'
    
    # Get all sheet names
    xl_file = pd.ExcelFile(excel_file)
    print("=" * 80)
    print(f"EXCEL FILE ANALYSIS: {excel_file}")
    print("=" * 80)
    print(f"\nTotal Sheets: {len(xl_file.sheet_names)}")
    print(f"Sheet Names: {xl_file.sheet_names}")
    print("\n" + "=" * 80)
    
    # Read each sheet
    for sheet_name in xl_file.sheet_names:
        print(f"\n📊 SHEET: {sheet_name}")
        print("-" * 80)
        
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        print(f"Rows: {len(df)}")
        print(f"Columns: {len(df.columns)}")
        print(f"\nColumn Names:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        print(f"\nData Types:")
        for col, dtype in df.dtypes.items():
            print(f"  {col}: {dtype}")
        
        print(f"\nFirst 5 Rows:")
        print(df.head().to_string())
        
        print(f"\nLast 5 Rows:")
        print(df.tail().to_string())
        
        print(f"\nBasic Statistics:")
        print(df.describe(include='all').to_string())
        
        print(f"\nMissing Values:")
        missing = df.isnull().sum()
        for col, count in missing.items():
            if count > 0:
                print(f"  {col}: {count} missing values")
        
        print(f"\nUnique Values per Column:")
        for col in df.columns:
            unique_count = df[col].nunique()
            print(f"  {col}: {unique_count} unique values")
            if unique_count <= 10:
                print(f"    Values: {df[col].unique().tolist()}")
        
        print("\n" + "=" * 80)

except Exception as e:
    print(f"Error reading Excel file: {e}")
    import traceback
    traceback.print_exc()
