import pandas as pd
import os
import json
from pathlib import Path

def analyze_excel_file(filepath):
    """Analyze an Excel file and return its structure"""
    try:
        # Try reading as HTML first (for .xls files that are actually HTML)
        if filepath.endswith('.xls'):
            try:
                df = pd.read_html(filepath)[0]
                source = "HTML"
            except:
                df = pd.read_excel(filepath)
                source = "Excel"
        else:
            df = pd.read_excel(filepath)
            source = "Excel"
        
        analysis = {
            "filename": os.path.basename(filepath),
            "source_format": source,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "sample_data": df.head(5).to_dict('records'),
            "null_counts": df.isnull().sum().to_dict(),
            "unique_values": {col: df[col].nunique() for col in df.columns}
        }
        return analysis
    except Exception as e:
        return {
            "filename": os.path.basename(filepath),
            "error": str(e)
        }

# Analyze all Excel files
excel_folder = "Excel"
results = {}

for filename in os.listdir(excel_folder):
    if filename.endswith(('.xls', '.xlsx')):
        filepath = os.path.join(excel_folder, filename)
        print(f"Analyzing: {filename}")
        results[filename] = analyze_excel_file(filepath)

# Save results
with open('excel_analysis_complete.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n=== ANALYSIS COMPLETE ===")
print(f"Total files analyzed: {len(results)}")
for filename, data in results.items():
    if 'error' in data:
        print(f"\n{filename}: ERROR - {data['error']}")
    else:
        print(f"\n{filename}:")
        print(f"  Format: {data['source_format']}")
        print(f"  Rows: {data['rows']}, Columns: {data['columns']}")
        print(f"  Columns: {', '.join(data['column_names'][:5])}{'...' if len(data['column_names']) > 5 else ''}")
