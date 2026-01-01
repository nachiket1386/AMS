# 📊 Database Tables - Simple Overview

## Quick Reference: All Tables & Columns

---

## 1️⃣ EMPLOYEES (Employee Master)
| Column | Type | Description |
|--------|------|-------------|
| **ep_no** 🔑 | VARCHAR(12) | Employee Number (Primary Key) |
| ep_name | VARCHAR(255) | Employee Name |
| contractor_id 🔗 | INTEGER | Contractor Code (Foreign Key) |
| sector_name | VARCHAR(100) | Sector Name |
| plant_name | VARCHAR(100) | Plant Name |
| department_name | VARCHAR(100) | Department Name |
| trade_name | VARCHAR(100) | Trade Name |
| skill | VARCHAR(50) | Skill Level |
| card_category | VARCHAR(50) | Card Category |
| created_at | DATETIME | Created Timestamp |
| updated_at | DATETIME | Updated Timestamp |

---

## 2️⃣ CONTRACTORS (Contractor Master)
| Column | Type | Description |
|--------|------|-------------|
| **contractor_code** 🔑 | INTEGER | Contractor Code (Primary Key) |
| contractor_name | VARCHAR(255) | Contractor Name |
| created_at | DATETIME | Created Timestamp |
| updated_at | DATETIME | Updated Timestamp |

---

## 3️⃣ PLANTS (Plant Master)
| Column | Type | Description |
|--------|------|-------------|
| **plant_code** 🔑 | VARCHAR(50) | Plant Code (Primary Key) |
| plant_name | VARCHAR(255) | Plant Name |
| sector_name | VARCHAR(100) | Sector Name |
| site_code | VARCHAR(50) | Site Code |
| site_desc | VARCHAR(255) | Site Description |
| created_at | DATETIME | Created Timestamp |

---

## 4️⃣ PUNCH_RECORDS (🕐 Punchrecord File)
| Column | Type | Description |
|--------|------|-------------|
| **id** 🔑 | INTEGER | Auto ID (Primary Key) |
| employee_id 🔗 | VARCHAR(12) | Employee Number (Foreign Key) |
| punchdate | DATE | Punch Date |
| shift | VARCHAR(50) | Shift |
| punch1_in | TIME | Punch 1 IN |
| punch2_out | TIME | Punch 2 OUT |
| punch3_in | TIME | Punch 3 IN |
| punch4_out | TIME | Punch 4 OUT |
| punch5_in | TIME | Punch 5 IN |
| punch6_out | TIME | Punch 6 OUT |
| early_in | TIME | Early IN |
| late_come | TIME | Late Come |
| early_out | TIME | Early OUT |
| hours_worked | TIME | Hours Worked |
| overstay | TIME | Overstay |
| overtime | TIME | Overtime |
| status | VARCHAR(10) | Status |
| regular_hours | TIME | Regular Hours |
| manual_request | BOOLEAN | Manual Request Flag |
| created_at | DATETIME | Created Timestamp |

---

## 5️⃣ DAILY_SUMMARY (📊 ARC Summary File)
| Column | Type | Description |
|--------|------|-------------|
| **id** 🔑 | INTEGER | Auto ID (Primary Key) |
| employee_id 🔗 | VARCHAR(12) | Employee Number (Foreign Key) |
| punchdate | DATE | Punch Date |
| mandays | DECIMAL(5,2) | Mandays |
| regular_manday_hr | TIME | Regular Manday Hours |
| ot | DECIMAL(5,2) | Overtime |
| location_status | VARCHAR(50) | Location Status |
| created_at | DATETIME | Created Timestamp |

---

## 6️⃣ OVERTIME_REQUESTS (⏰ Overtime File)
| Column | Type | Description |
|--------|------|-------------|
| **id** 🔑 | INTEGER | Auto ID (Primary Key) |
| employee_id 🔗 | VARCHAR(12) | Employee Number (Foreign Key) |
| punchdate | DATE | Punch Date |
| actual_overstay | TIME | Actual Overstay |
| requested_overtime | TIME | Requested Overtime |
| approved_overtime | TIME | Approved Overtime |
| requested_regular_hours | TIME | Requested Regular Hours |
| approved_regular_hours | TIME | Approved Regular Hours |
| contractor_request_date | DATETIME | Contractor Request Date |
| contractor_remarks | TEXT | Contractor Remarks |
| contractor_reason | TEXT | Contractor Reason |
| actual_eic_code | INTEGER | Actual EIC Code |
| requested_eic_code | INTEGER | Requested EIC Code |
| eic_approve_date | DATETIME | EIC Approve Date |
| eic_remarks | TEXT | EIC Remarks |
| status | VARCHAR(20) | Status (Pending/Approved/Rejected) |
| created_at | DATETIME | Created Timestamp |

---

## 7️⃣ PARTIAL_DAY_REQUESTS (📅 Partial Day File)
| Column | Type | Description |
|--------|------|-------------|
| **id** 🔑 | INTEGER | Auto ID (Primary Key) |
| employee_id 🔗 | VARCHAR(12) | Employee Number (Foreign Key) |
| punchdate | DATE | Punch Date |
| actual_pd_hours | TIME | Actual PD Hours |
| requested_pd_hours | TIME | Requested PD Hours |
| approved_pd_hours | TIME | Approved PD Hours |
| manday_conversion | DECIMAL(3,2) | Manday Conversion |
| contractor_request_date | DATETIME | Contractor Request Date |
| contractor_remarks | TEXT | Contractor Remarks |
| eic_code | INTEGER | EIC Code |
| eic_approve_date | DATETIME | EIC Approve Date |
| eic_remarks | TEXT | EIC Remarks |
| status | VARCHAR(20) | Status (Pending/Approved/Rejected) |
| created_at | DATETIME | Created Timestamp |

---

## 8️⃣ REGULARIZATION_REQUESTS (✏️ Regularization File)
| Column | Type | Description |
|--------|------|-------------|
| **id** 🔑 | INTEGER | Auto ID (Primary Key) |
| employee_id 🔗 | VARCHAR(12) | Employee Number (Foreign Key) |
| punchdate | DATE | Punch Date |
| old_punch_in | TIME | Old Punch IN |
| old_punch_out | TIME | Old Punch OUT |
| new_punch_in | TIME | New Punch IN |
| new_punch_out | TIME | New Punch OUT |
| contractor_request_date | DATETIME | Contractor Request Date |
| contractor_remarks | TEXT | Contractor Remarks |
| contractor_reason | TEXT | Contractor Reason |
| eic_code | INTEGER | EIC Code |
| eic_approve_date | DATETIME | EIC Approve Date |
| eic_remarks | TEXT | EIC Remarks |
| status | VARCHAR(20) | Status (Pending/Approved/Rejected) |
| created_at | DATETIME | Created Timestamp |

---

## 9️⃣ IMPORT_LOGS (Import History)
| Column | Type | Description |
|--------|------|-------------|
| **id** 🔑 | INTEGER | Auto ID (Primary Key) |
| user_id 🔗 | INTEGER | User ID (Foreign Key) |
| filename | VARCHAR(255) | Uploaded Filename |
| file_type | VARCHAR(50) | File Type |
| total_rows | INTEGER | Total Rows |
| imported_rows | INTEGER | Successfully Imported Rows |
| duplicate_rows | INTEGER | Duplicate Rows Skipped |
| error_rows | INTEGER | Error Rows |
| status | VARCHAR(20) | Import Status |
| error_report_path | VARCHAR(500) | Error Report File Path |
| created_at | DATETIME | Import Timestamp |

---

## 🔟 EXPORT_LOGS (Export History)
| Column | Type | Description |
|--------|------|-------------|
| **id** 🔑 | INTEGER | Auto ID (Primary Key) |
| user_id 🔗 | INTEGER | User ID (Foreign Key) |
| export_type | VARCHAR(50) | Export Type |
| record_count | INTEGER | Number of Records Exported |
| filters | JSON | Applied Filters |
| created_at | DATETIME | Export Timestamp |

---

## 1️⃣1️⃣ UPLOAD_PERMISSIONS (User Permissions)
| Column | Type | Description |
|--------|------|-------------|
| **id** 🔑 | INTEGER | Auto ID (Primary Key) |
| user_id 🔗 | INTEGER | User ID (Foreign Key) |
| file_type | VARCHAR(50) | File Type |
| can_upload | BOOLEAN | Upload Permission Flag |
| granted_by_id 🔗 | INTEGER | Granted By User ID (Foreign Key) |
| granted_at | DATETIME | Permission Granted Timestamp |

---

## 🔗 Relationships

```
CONTRACTORS (1) ──────► (N) EMPLOYEES
                              │
                              ├──► (N) PUNCH_RECORDS
                              ├──► (N) DAILY_SUMMARY
                              ├──► (N) OVERTIME_REQUESTS
                              ├──► (N) PARTIAL_DAY_REQUESTS
                              └──► (N) REGULARIZATION_REQUESTS

AUTH_USER (1) ──────► (N) IMPORT_LOGS
              ──────► (N) EXPORT_LOGS
              ──────► (N) UPLOAD_PERMISSIONS

PLANTS (Independent reference table)
```

---

## 📋 Summary

| # | Table Name | Columns | Purpose |
|---|-----------|---------|---------|
| 1 | employees | 11 | Employee master data |
| 2 | contractors | 4 | Contractor master data |
| 3 | plants | 6 | Plant/location master data |
| 4 | punch_records | 19 | Punch in/out records |
| 5 | daily_summary | 8 | Daily attendance summary |
| 6 | overtime_requests | 17 | Overtime requests |
| 7 | partial_day_requests | 14 | Partial day requests |
| 8 | regularization_requests | 14 | Regularization requests |
| 9 | import_logs | 11 | Import history & audit |
| 10 | export_logs | 6 | Export history & audit |
| 11 | upload_permissions | 6 | User upload permissions |

**Total: 11 Tables, 116 Columns**

---

## 🎯 Key Points

✅ **3 Master Tables** - Reference data (employees, contractors, plants)  
✅ **5 Transaction Tables** - Daily attendance data  
✅ **3 Audit Tables** - Logs and permissions  
✅ **Foreign Keys** - Data integrity maintained  
✅ **Indexes** - Fast query performance  
✅ **Unique Constraints** - No duplicate records  

---

**All Excel file data is stored in these tables with complete audit trails!** 🎉
