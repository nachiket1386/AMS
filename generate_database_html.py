"""
Generate HTML documentation for database schema
"""

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Schema - Excel Upload System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; color: #333; }
        .container { max-width: 1400px; margin: 0 auto; background: white; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden; }
        .header { background: linear-gradient(135deg, #4A70A9 0%, #8FABD4 100%); color: white; padding: 40px; text-align: center; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
        .header p { font-size: 1.2rem; opacity: 0.9; }
        .nav-tabs { display: flex; background: #f5f5f5; border-bottom: 2px solid #ddd; overflow-x: auto; flex-wrap: wrap; }
        .nav-tab { padding: 15px 25px; cursor: pointer; border: none; background: transparent; font-size: 1rem; font-weight: 600; color: #666; transition: all 0.3s; white-space: nowrap; }
        .nav-tab:hover { background: #e0e0e0; color: #4A70A9; }
        .nav-tab.active { background: white; color: #4A70A9; border-bottom: 3px solid #4A70A9; }
        .content { padding: 40px; }
        .tab-content { display: none; }
        .tab-content.active { display: block; animation: fadeIn 0.5s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .table-card { background: white; border: 2px solid #8FABD4; border-radius: 15px; padding: 25px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s, box-shadow 0.3s; }
        .table-card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.2); }
        .table-card h3 { color: #4A70A9; font-size: 1.5rem; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
        .table-icon { font-size: 2rem; }
        .table-info { background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .table-info p { margin: 5px 0; font-size: 0.95rem; }
        .columns-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .columns-table th { background: #4A70A9; color: white; padding: 12px; text-align: left; font-weight: 600; }
        .columns-table td { padding: 10px 12px; border-bottom: 1px solid #e0e0e0; }
        .columns-table tr:hover { background: #f5f5f5; }
        .pk-badge { background: #ff6b6b; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; margin-right: 5px; }
        .fk-badge { background: #4ecdc4; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; margin-right: 5px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }
        .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .stat-card h3 { font-size: 2.5rem; margin-bottom: 10px; }
        .stat-card p { font-size: 1rem; opacity: 0.9; }
        .mapping-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        .mapping-table th { background: #4A70A9; color: white; padding: 15px; text-align: left; font-size: 1.1rem; }
        .mapping-table td { padding: 15px; border-bottom: 1px solid #e0e0e0; font-size: 1rem; }
        .mapping-table tr:hover { background: #f5f5f5; }
        .flow-box { background: white; border: 3px solid #8FABD4; border-radius: 15px; padding: 20px; margin: 20px 0; text-align: center; position: relative; }
        .flow-arrow { text-align: center; font-size: 2rem; color: #4A70A9; margin: 10px 0; }
        @media (max-width: 768px) { .header h1 { font-size: 1.8rem; } .content { padding: 20px; } .stats-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Database Schema Documentation</h1>
            <p>Excel File Upload System - Complete Database Structure</p>
        </div>
"""

# Write to file
with open('database_schema_visual.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML file created successfully!")
print("Run: python generate_database_html.py")
