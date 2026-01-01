import sqlite3
import sys

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()

print("=" * 80)
print("DATABASE TABLES IN SQLite")
print("=" * 80)
print()

for table in tables:
    table_name = table[0]
    
    # Skip Django internal tables for cleaner output
    if table_name.startswith('django_') or table_name.startswith('auth_') or table_name.startswith('sqlite_'):
        continue
    
    print(f"\n📊 TABLE: {table_name}")
    print("-" * 80)
    
    # Get table schema
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    
    print(f"{'Column Name':<30} {'Type':<15} {'Null':<8} {'Default':<15} {'PK'}")
    print("-" * 80)
    
    for col in columns:
        col_id, col_name, col_type, not_null, default_val, is_pk = col
        null_str = "NO" if not_null else "YES"
        default_str = str(default_val) if default_val is not None else ""
        pk_str = "✓" if is_pk else ""
        
        print(f"{col_name:<30} {col_type:<15} {null_str:<8} {default_str:<15} {pk_str}")
    
    # Get row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cursor.fetchone()[0]
    print(f"\n📈 Total Records: {count}")
    
    # Get indexes
    cursor.execute(f"PRAGMA index_list({table_name});")
    indexes = cursor.fetchall()
    if indexes:
        print(f"\n🔍 Indexes:")
        for idx in indexes:
            idx_name = idx[1]
            cursor.execute(f"PRAGMA index_info({idx_name});")
            idx_cols = cursor.fetchall()
            col_names = [col[2] for col in idx_cols]
            print(f"  - {idx_name}: {', '.join(col_names)}")

print("\n" + "=" * 80)
print("END OF DATABASE SCHEMA")
print("=" * 80)

conn.close()
