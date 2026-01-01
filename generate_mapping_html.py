#!/usr/bin/env python3
"""
Generate complete HTML file with Excel to Database column mapping
"""

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Schema with Excel Mapping</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; color: #333; }
        .container { max-width: 1400px; margin: 0 auto; background: white; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden; }
        .header { background: linear-gradient(135deg, #4A70A9 0%, #8FABD4 100%); color: white; padding: 40px; text-align: center; position: relative; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .header p { font-size: 1.2rem; opacity: 0.9; }
        .content { padding: 40px; }
        .file-card { background: white; border: 3px solid #8FABD4; border-radius: 15px; padding: 25px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s; }
        .file-card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.2); }
        .file-card h2 { color: #4A70A9; margin-bottom: 15px; font-size: 1.8rem; display: flex; align-items: center; gap: 10px; }
        .file-info { background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .file-info p { margin: 5px 0; font-size: 0.95rem; }
        .mapping-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .mapping-table th { background: #4A70A9; color: white; padding: 12px; text-align: left; font-weight: 600; font-size: 1rem; }
        .mapping-table td { padding: 10px 12px; border-bottom: 1px solid #e0e0e0; font-size: 0.95rem; }
        .mapping-table tr:hover { background: #f5f5f5; }
        .excel-col { color: #e74c3c; font-weight: 600; font-family: 'Courier New', monospace; }
        .db-col { color: #27ae60; font-weight: 600; font-family: 'Courier New', monospace; }
        .arrow { color: #4A70A9; font-size: 1.5rem; font-weight: bold; }
        .type-badge { background: #3498db; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
        @media print { body { background: white; padding: 0; } .file-card { page-break-inside: avoid; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Database Schema with Excel File Mapping</h1>
            <p>Complete Column Mapping: Excel Files ↔ Database Tables</p>
        </div>
        <div class="content">
"""

# File 1: Punchrecord
html_content += """
            <div class="file-card">
                <h2>🕐 File 1: Punchrecord Report</h2>
                <div class="file-info">
                    <p><strong>Excel File:</strong> Punchrecord Report (6).xls</p>
                    <p><strong>Database Table:</strong> punch_records</p>
                    <p><strong>Purpose:</strong> Detailed punch-in/punch-out records</p>
                    <p><strong>Records:</strong> 25,071 rows</p>
                </div>
                <table class="mapping-table">
                    <thead>
                        <tr>
                            <th>Excel Column Header</th>
                            <th></th>
                            <th>Database Column Name</th>
                            <th>Data Type</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="excel-col">EP NO</td><td class="arrow">→</td><td class="db-col">employee_id</td><td><span class="type-badge">VARCHAR(12)</span></td></tr>
                        <tr><td class="excel-col">PUNCHDATE</td><td class="arrow">→</td><td class="db-col">punchdate</td><td><span class="type-badge">DATE</span></td></tr>
                        <tr><td class="excel-col">SHIFT</td><td class="arrow">→</td><td class="db-col">shift</td><td><span class="type-badge">VARCHAR(50)</span></td></tr>
                        <tr><td class="excel-col">PUNCH1 IN</td><td class="arrow">→</td><td class="db-col">punch1_in</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">PUNCH2 OUT</td><td class="arrow">→</td><td class="db-col">punch2_out</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">PUNCH3 IN</td><td class="arrow">→</td><td class="db-col">punch3_in</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">PUNCH4 OUT</td><td class="arrow">→</td><td class="db-col">punch4_out</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">PUNCH5 IN</td><td class="arrow">→</td><td class="db-col">punch5_in</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">PUNCH6 OUT</td><td class="arrow">→</td><td class="db-col">punch6_out</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">EARLY IN</td><td class="arrow">→</td><td class="db-col">early_in</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">LATE COME</td><td class="arrow">→</td><td class="db-col">late_come</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">EARLY OUT</td><td class="arrow">→</td><td class="db-col">early_out</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">HOURS WORKED</td><td class="arrow">→</td><td class="db-col">hours_worked</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">OVERSTAY</td><td class="arrow">→</td><td class="db-col">overstay</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">OVERTIME</td><td class="arrow">→</td><td class="db-col">overtime</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">STATUS</td><td class="arrow">→</td><td class="db-col">status</td><td><span class="type-badge">VARCHAR(10)</span></td></tr>
                        <tr><td class="excel-col">REGULAR HOURS</td><td class="arrow">→</td><td class="db-col">regular_hours</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">MANUAL REQUEST</td><td class="arrow">→</td><td class="db-col">manual_request</td><td><span class="type-badge">BOOLEAN</span></td></tr>
                    </tbody>
                </table>
            </div>
"""

# File 2: ARC Summary
html_content += """
            <div class="file-card">
                <h2>📊 File 2: Date wise ARC Summary</h2>
                <div class="file-info">
                    <p><strong>Excel File:</strong> Date wise ARC Summary (1).xls</p>
                    <p><strong>Database Table:</strong> daily_summary</p>
                    <p><strong>Purpose:</strong> Daily attendance summary with mandays</p>
                    <p><strong>Records:</strong> 15,496 rows</p>
                </div>
                <table class="mapping-table">
                    <thead>
                        <tr>
                            <th>Excel Column Header</th>
                            <th></th>
                            <th>Database Column Name</th>
                            <th>Data Type</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="excel-col">epNo</td><td class="arrow">→</td><td class="db-col">employee_id</td><td><span class="type-badge">VARCHAR(12)</span></td></tr>
                        <tr><td class="excel-col">punchDate</td><td class="arrow">→</td><td class="db-col">punchdate</td><td><span class="type-badge">DATE</span></td></tr>
                        <tr><td class="excel-col">mandays</td><td class="arrow">→</td><td class="db-col">mandays</td><td><span class="type-badge">DECIMAL(5,2)</span></td></tr>
                        <tr><td class="excel-col">regularMandayHr</td><td class="arrow">→</td><td class="db-col">regular_manday_hr</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">ot</td><td class="arrow">→</td><td class="db-col">ot</td><td><span class="type-badge">DECIMAL(5,2)</span></td></tr>
                        <tr><td class="excel-col">locationStatus</td><td class="arrow">→</td><td class="db-col">location_status</td><td><span class="type-badge">VARCHAR(50)</span></td></tr>
                    </tbody>
                </table>
            </div>
"""

# File 3: Overtime
html_content += """
            <div class="file-card">
                <h2>⏰ File 3: Overtime Requests</h2>
                <div class="file-info">
                    <p><strong>Excel File:</strong> OVERTIME (2).xls</p>
                    <p><strong>Database Table:</strong> overtime_requests</p>
                    <p><strong>Purpose:</strong> Overtime request and approval tracking</p>
                    <p><strong>Records:</strong> 770 rows</p>
                </div>
                <table class="mapping-table">
                    <thead>
                        <tr>
                            <th>Excel Column Header</th>
                            <th></th>
                            <th>Database Column Name</th>
                            <th>Data Type</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="excel-col">EP NO</td><td class="arrow">→</td><td class="db-col">employee_id</td><td><span class="type-badge">VARCHAR(12)</span></td></tr>
                        <tr><td class="excel-col">PUNCHDATE</td><td class="arrow">→</td><td class="db-col">punchdate</td><td><span class="type-badge">DATE</span></td></tr>
                        <tr><td class="excel-col">ACTUAL OVERSTAY</td><td class="arrow">→</td><td class="db-col">actual_overstay</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">REQUESTED OVERTIME</td><td class="arrow">→</td><td class="db-col">requested_overtime</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">APPROVED OVERTIME</td><td class="arrow">→</td><td class="db-col">approved_overtime</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">REQUESTED REGULAR HOURS</td><td class="arrow">→</td><td class="db-col">requested_regular_hours</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">APPROVED REGULAR HOURS</td><td class="arrow">→</td><td class="db-col">approved_regular_hours</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">CONTRACTOR OT REQUEST DATE</td><td class="arrow">→</td><td class="db-col">contractor_request_date</td><td><span class="type-badge">DATETIME</span></td></tr>
                        <tr><td class="excel-col">CONTRACTOR REMARKS</td><td class="arrow">→</td><td class="db-col">contractor_remarks</td><td><span class="type-badge">TEXT</span></td></tr>
                        <tr><td class="excel-col">CONTRACTOR REASON</td><td class="arrow">→</td><td class="db-col">contractor_reason</td><td><span class="type-badge">TEXT</span></td></tr>
                        <tr><td class="excel-col">ACTUAL EIC CODE</td><td class="arrow">→</td><td class="db-col">actual_eic_code</td><td><span class="type-badge">INTEGER</span></td></tr>
                        <tr><td class="excel-col">REQUESTED EIC CODE</td><td class="arrow">→</td><td class="db-col">requested_eic_code</td><td><span class="type-badge">INTEGER</span></td></tr>
                        <tr><td class="excel-col">EIC APPROVE/REJECT DATE</td><td class="arrow">→</td><td class="db-col">eic_approve_date</td><td><span class="type-badge">DATETIME</span></td></tr>
                        <tr><td class="excel-col">EIC REQUEST REMARKS</td><td class="arrow">→</td><td class="db-col">eic_remarks</td><td><span class="type-badge">TEXT</span></td></tr>
                        <tr><td class="excel-col">OT REQUEST STATUS</td><td class="arrow">→</td><td class="db-col">status</td><td><span class="type-badge">VARCHAR(20)</span></td></tr>
                    </tbody>
                </table>
            </div>
"""

# File 4: Partial Day
html_content += """
            <div class="file-card">
                <h2>📅 File 4: Partial Day Requests</h2>
                <div class="file-info">
                    <p><strong>Excel File:</strong> PARTIAL DAY.xls</p>
                    <p><strong>Database Table:</strong> partial_day_requests</p>
                    <p><strong>Purpose:</strong> Partial day work requests</p>
                    <p><strong>Records:</strong> 19 rows</p>
                </div>
                <table class="mapping-table">
                    <thead>
                        <tr>
                            <th>Excel Column Header</th>
                            <th></th>
                            <th>Database Column Name</th>
                            <th>Data Type</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="excel-col">EP NO</td><td class="arrow">→</td><td class="db-col">employee_id</td><td><span class="type-badge">VARCHAR(12)</span></td></tr>
                        <tr><td class="excel-col">PUNCHDATE</td><td class="arrow">→</td><td class="db-col">punchdate</td><td><span class="type-badge">DATE</span></td></tr>
                        <tr><td class="excel-col">ACTUAL PD HOURS</td><td class="arrow">→</td><td class="db-col">actual_pd_hours</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">REQUESTED PD HOURS</td><td class="arrow">→</td><td class="db-col">requested_pd_hours</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">APPROVED PD HOURS</td><td class="arrow">→</td><td class="db-col">approved_pd_hours</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">MANDAY CONVERSION</td><td class="arrow">→</td><td class="db-col">manday_conversion</td><td><span class="type-badge">DECIMAL(3,2)</span></td></tr>
                        <tr><td class="excel-col">CONTRACTOR PD REQUEST DATE</td><td class="arrow">→</td><td class="db-col">contractor_request_date</td><td><span class="type-badge">DATETIME</span></td></tr>
                        <tr><td class="excel-col">CONTRACTOR REMARKS</td><td class="arrow">→</td><td class="db-col">contractor_remarks</td><td><span class="type-badge">TEXT</span></td></tr>
                        <tr><td class="excel-col">EIC CODE</td><td class="arrow">→</td><td class="db-col">eic_code</td><td><span class="type-badge">INTEGER</span></td></tr>
                        <tr><td class="excel-col">EIC APPROVE/REJECT DATE</td><td class="arrow">→</td><td class="db-col">eic_approve_date</td><td><span class="type-badge">DATETIME</span></td></tr>
                        <tr><td class="excel-col">EIC REQUEST REMARKS</td><td class="arrow">→</td><td class="db-col">eic_remarks</td><td><span class="type-badge">TEXT</span></td></tr>
                        <tr><td class="excel-col">PD REQUEST STATUS</td><td class="arrow">→</td><td class="db-col">status</td><td><span class="type-badge">VARCHAR(20)</span></td></tr>
                    </tbody>
                </table>
            </div>
"""

# File 5: Regularization
html_content += """
            <div class="file-card">
                <h2>✏️ File 5: Regularization Audit Report</h2>
                <div class="file-info">
                    <p><strong>Excel File:</strong> Regularization Audit Report (1).xls</p>
                    <p><strong>Database Table:</strong> regularization_requests</p>
                    <p><strong>Purpose:</strong> Punch time correction requests</p>
                    <p><strong>Records:</strong> 146 rows</p>
                </div>
                <table class="mapping-table">
                    <thead>
                        <tr>
                            <th>Excel Column Header</th>
                            <th></th>
                            <th>Database Column Name</th>
                            <th>Data Type</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td class="excel-col">EP NO</td><td class="arrow">→</td><td class="db-col">employee_id</td><td><span class="type-badge">VARCHAR(12)</span></td></tr>
                        <tr><td class="excel-col">PUNCHDATE</td><td class="arrow">→</td><td class="db-col">punchdate</td><td><span class="type-badge">DATE</span></td></tr>
                        <tr><td class="excel-col">OLD PUNCH IN</td><td class="arrow">→</td><td class="db-col">old_punch_in</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">OLD PUNCH OUT</td><td class="arrow">→</td><td class="db-col">old_punch_out</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">NEW PUNCH IN</td><td class="arrow">→</td><td class="db-col">new_punch_in</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">NEW PUNCH OUT</td><td class="arrow">→</td><td class="db-col">new_punch_out</td><td><span class="type-badge">TIME</span></td></tr>
                        <tr><td class="excel-col">CONTRACTOR REQUEST DATE</td><td class="arrow">→</td><td class="db-col">contractor_request_date</td><td><span class="type-badge">DATETIME</span></td></tr>
                        <tr><td class="excel-col">CONTRACTOR REMARKS</td><td class="arrow">→</td><td class="db-col">contractor_remarks</td><td><span class="type-badge">TEXT</span></td></tr>
                        <tr><td class="excel-col">CONTRACTOR REASON</td><td class="arrow">→</td><td class="db-col">contractor_reason</td><td><span class="type-badge">TEXT</span></td></tr>
                        <tr><td class="excel-col">EIC CODE</td><td class="arrow">→</td><td class="db-col">eic_code</td><td><span class="type-badge">INTEGER</span></td></tr>
                        <tr><td class="excel-col">EIC APPROVE/REJECT DATE</td><td class="arrow">→</td><td class="db-col">eic_approve_date</td><td><span class="type-badge">DATETIME</span></td></tr>
                        <tr><td class="excel-col">EIC REQUEST REMARKS</td><td class="arrow">→</td><td class="db-col">eic_remarks</td><td><span class="type-badge">TEXT</span></td></tr>
                        <tr><td class="excel-col">REQUEST STATUS</td><td class="arrow">→</td><td class="db-col">status</td><td><span class="type-badge">VARCHAR(20)</span></td></tr>
                    </tbody>
                </table>
            </div>
"""

html_content += """
        </div>
    </div>
</body>
</html>
"""

# Write to file
with open('database_schema_visual.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ HTML file created successfully!")
print("📄 File: database_schema_visual.html")
print("🚀 Open it in your browser to view the complete mapping!")
