import pandas as pd
import json

files = [
    'Excel/Date wise ARC Summary (1).xls',
    'Excel/OVERTIME (2).xls',
    'Excel/PARTIAL DAY.xls',
    'Excel/Punchrecord Report (6).xls',
    'Excel/Regularization Audit Report (1).xls'
]

results = {}

for file_path in files:
    try:
        df = pd.read_excel(file_path, engine='xlrd')
        file_name = file_path.split('/')[-1]
        
        results[file_name] = {
            'columns': list(df.columns),
            'row_count': len(df),
            'column_count': len(df.columns),
            'sample_data': df.head(3).to_dict('records'),
            'data_types': {col: str(dtype) for col, dtype in df.dtypes.items()}
        }
        
        print(f"\n{'='*70}")
        print(f"FILE: {file_name}")
        print(f"{'='*70}")
        print(f"Columns ({len(df.columns)}): {list(df.columns)}")
        print(f"Rows: {len(df)}")
        print(f"\nFirst 3 rows:")
        print(df.head(3).to_string())
        
    except Exception as e:
        print(f"\nError reading {file_path}: {e}")
        results[file_path] = {'error': str(e)}

# Save to JSON
with open('Excel/excel_files_analysis.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"\n\n{'='*70}")
print("Analysis saved to: Excel/excel_files_analysis.json")
print(f"{'='*70}")
