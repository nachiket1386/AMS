# Database Schema Documentation
## Attendance Management System

This document describes all database tables in the system with sample data.

---

## Table 1: `core_company`
**Purpose:** Stores company information for multi-tenant data isolation

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| name | VARCHAR(255) | Company name (unique) |
| created_at | DATETIME | When company was created |

**Sample Data:**
```
id | name                              | created_at
---|-----------------------------------|-------------------
1  | ADAGE AUTOMATION PVT LTD          | 2025-01-15 10:30:00
2  | AVON ENGINEERING                  | 2025-01-16 11:45:00
3  | BUREAU VERITAS (INDIA) PVT LTD    | 2025-01-17 09:20:00
4  | CREATIVE INFOTECH SOLUTIONS       | 2025-01-18 14:10:00
5  | IDEAL HANDLING PVT LTD            | 2025-01-19 16:55:00
```

---

## Table 2: `core_user`
**Purpose:** User accounts with role-based access control

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| username | VARCHAR(150) | Login username (unique) |
| email | VARCHAR(254) | Email address |
| password | VARCHAR(128) | Hashed password |
| first_name | VARCHAR(150) | First name |
| last_name | VARCHAR(150) | Last name |
| role | VARCHAR(10) | User role: root/admin/user1 |
| company_id | INTEGER | Foreign Key to core_company |
| assigned_date_from | DATE | Access start date (User1 only) |
| assigned_date_to | DATE | Access end date (User1 only) |
| is_active | BOOLEAN | Account active status |
| is_staff | BOOLEAN | Django admin access |
| is_superuser | BOOLEAN | Superuser status |
| date_joined | DATETIME | Account creation date |

**Sample Data:**
```
id | username  | email              | role   | company_id | assigned_date_from | assigned_date_to | is_active
---|-----------|--------------------| -------|------------|--------------------|--------------------|----------
1  | root      | root@system.com    | root   | NULL       | NULL               | NULL               | 1
2  | admin1    | admin1@adage.com   | admin  | 1          | NULL               | NULL               | 1
3  | admin2    | admin2@avon.com    | admin  | 2          | NULL               | NULL               | 1
4  | user1_a   | user1@adage.com    | user1  | 1          | 2025-01-01         | 2025-12-31         | 1
5  | user1_b   | user1@avon.com     | user1  | 2          | 2025-06-01         | 2025-12-31         | 1
```

---

## Table 3: `core_attendancerecord`
**Purpose:** Stores daily attendance records for employees

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| ep_no | VARCHAR(50) | Employee number |
| ep_name | VARCHAR(255) | Employee name |
| date | DATE | Attendance date |
| company_id | INTEGER | Foreign Key to core_company |
| shift | VARCHAR(100) | Shift code/name |
| time_in_1 | VARCHAR(20) | First check-in time |
| time_out_1 | VARCHAR(20) | First check-out time |
| time_in_2 | VARCHAR(20) | Second check-in time |
| time_out_2 | VARCHAR(20) | Second check-out time |
| time_in_3 | VARCHAR(20) | Third check-in time |
| time_out_3 | VARCHAR(20) | Third check-out time |
| time_in_4 | VARCHAR(20) | Fourth check-in time |
| time_out_4 | VARCHAR(20) | Fourth check-out time |
| hours | VARCHAR(20) | Total hours worked |
| overstay | VARCHAR(20) | Overstay hours |
| status | VARCHAR(10) | Status: P/A/PH/WO/PD/-0.5/-1 |
| overtime | VARCHAR(20) | Overtime hours |
| overtime_to_mandays | DECIMAL(5,2) | Overtime in mandays |
| created_at | DATETIME | Record creation time |
| updated_at | DATETIME | Last update time |

**Sample Data:**
```
id  | ep_no         | ep_name           | date       | company_id | shift | time_in_1 | time_out_1 | hours | overstay | status | overtime | overtime_to_mandays
----|---------------|-------------------|------------|------------|-------|-----------|------------|-------|----------|--------|----------|--------------------
1   | PP5000012345  | RAJESH KUMAR      | 2025-12-13 | 1          | G     | 08:00     | 17:00      | 09:00 | 01:00    | P      | 01:00    | 0.13
2   | PP5000012346  | AMIT PATEL        | 2025-12-13 | 1          | G     | 08:15     | 17:30      | 09:15 | 01:30    | P      | 01:30    | 0.19
3   | PP5000012347  | SURESH SINGH      | 2025-12-13 | 2          | N     | 20:00     | 05:00      | 09:00 | 00:00    | P      | 00:00    | 0.00
4   | PP5000012348  | VIJAY SHARMA      | 2025-12-13 | 1          | G     | -         | -          | -     | -        | A      | -        | NULL
5   | PP5000012349  | PRAKASH MEHTA     | 2025-12-13 | 2          | G     | 08:00     | 17:45      | 09:45 | 01:45    | P      | 01:45    | 0.22
```

---

## Table 4: `remark_reasons`
**Purpose:** Categories/reasons for remarks (managed by Admin)

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| company_id | INTEGER | Foreign Key to core_company |
| reason | VARCHAR(255) | Reason/category name |
| is_active | BOOLEAN | Active status |
| created_by_id | INTEGER | Foreign Key to core_user |
| created_at | DATETIME | Creation timestamp |

**Sample Data:**
```
id | company_id | reason                    | is_active | created_by_id | created_at
---|------------|---------------------------|-----------|---------------|-------------------
1  | 1          | Overtime Request          | 1         | 2             | 2025-12-01 10:00:00
2  | 1          | Regularization            | 1         | 2             | 2025-12-01 10:05:00
3  | 1          | Leave Adjustment          | 1         | 2             | 2025-12-01 10:10:00
4  | 2          | Time Correction           | 1         | 3             | 2025-12-02 11:00:00
5  | 2          | Shift Change Request      | 1         | 3             | 2025-12-02 11:15:00
```

---

## Table 5: `attendance_remarks`
**Purpose:** Remarks added by User1 for attendance records

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| attendance_record_id | INTEGER | Foreign Key to core_attendancerecord |
| ep_no | VARCHAR(50) | Employee number |
| date | DATE | Attendance date |
| reason_id | INTEGER | Foreign Key to remark_reasons |
| remarks_text | TEXT | Detailed remarks/comments |
| created_by_id | INTEGER | Foreign Key to core_user (User1) |
| created_at | DATETIME | When remark was created |
| updated_at | DATETIME | Last update time |
| admin_response | TEXT | Admin's response |
| responded_by_id | INTEGER | Foreign Key to core_user (Admin) |
| responded_at | DATETIME | When admin responded |
| status | VARCHAR(20) | pending/reviewed/resolved |

**Sample Data:**
```
id | attendance_record_id | ep_no        | date       | reason_id | remarks_text                                          | created_by_id | created_at          | status   | admin_response
---|----------------------|--------------|------------|-----------|-------------------------------------------------------|---------------|---------------------|----------|----------------
1  | 1                    | PP5000012345 | 2025-12-13 | 1         | Worked extra 1 hour for urgent project delivery      | 4             | 2025-12-14 09:30:00 | pending  | NULL
2  | 2                    | PP5000012346 | 2025-12-13 | 2         | Forgot to punch out, actually left at 17:00           | 4             | 2025-12-14 10:15:00 | reviewed | Will update
3  | 5                    | PP5000012349 | 2025-12-13 | 1         | Extended shift for client meeting                     | 5             | 2025-12-14 11:00:00 | resolved | Approved
4  | 1                    | PP5000012345 | 2025-12-12 | 3         | Was on approved leave but marked present              | 4             | 2025-12-13 14:20:00 | pending  | NULL
5  | 2                    | PP5000012346 | 2025-12-12 | 4         | Check-in time should be 08:00 not 08:15               | 4             | 2025-12-13 15:45:00 | reviewed | Correcting
```

---

## Table 6: `import_logs`
**Purpose:** Tracks file upload history

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key to core_user |
| filename | VARCHAR(255) | Uploaded file name |
| file_type | VARCHAR(20) | attendance/mandays/punchrecord |
| status | VARCHAR(20) | success/error/partial |
| total_rows | INTEGER | Total rows in file |
| success_rows | INTEGER | Successfully imported rows |
| error_rows | INTEGER | Failed rows |
| error_report_path | VARCHAR(500) | Path to error report |
| created_at | DATETIME | Upload timestamp |

**Sample Data:**
```
id | user_id | filename                    | file_type  | status  | total_rows | success_rows | error_rows | created_at
---|---------|-----------------------------| -----------|---------|------------|--------------|------------|-------------------
1  | 2       | attendance_dec_2025.xlsx    | attendance | success | 500        | 500          | 0          | 2025-12-01 10:00:00
2  | 2       | attendance_nov_2025.xlsx    | attendance | partial | 450        | 445          | 5          | 2025-11-30 15:30:00
3  | 3       | punchrecord_dec_2025.xlsx   | punchrecord| success | 1200       | 1200         | 0          | 2025-12-05 09:15:00
4  | 1       | mandays_dec_2025.xlsx       | mandays    | success | 300        | 300          | 0          | 2025-12-10 11:45:00
5  | 2       | attendance_oct_2025.xlsx    | attendance | error   | 400        | 0            | 400        | 2025-10-31 16:20:00
```

---

## Table 7: `export_log`
**Purpose:** Tracks data export history

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key to core_user |
| export_type | VARCHAR(50) | Type of export |
| filename | VARCHAR(255) | Generated filename |
| record_count | INTEGER | Number of records exported |
| created_at | DATETIME | Export timestamp |

**Sample Data:**
```
id | user_id | export_type      | filename                           | record_count | created_at
---|---------|------------------|------------------------------------|--------------|-------------------
1  | 2       | attendance       | attendance_20251201_103045.xlsx    | 500          | 2025-12-01 10:30:45
2  | 3       | remarks_log      | remarks_log_20251214_143022.xlsx   | 25           | 2025-12-14 14:30:22
3  | 1       | attendance       | attendance_20251210_091520.xlsx    | 5000         | 2025-12-10 09:15:20
4  | 2       | mandays          | mandays_20251205_160033.xlsx       | 300          | 2025-12-05 16:00:33
5  | 3       | punchrecord      | punchrecord_20251215_113045.xlsx   | 1200         | 2025-12-15 11:30:45
```

---

## Relationships Diagram

```
core_company (1) ----< (N) core_user
core_company (1) ----< (N) core_attendancerecord
core_company (1) ----< (N) remark_reasons

core_user (1) ----< (N) remark_reasons (created_by)
core_user (1) ----< (N) attendance_remarks (created_by)
core_user (1) ----< (N) attendance_remarks (responded_by)
core_user (1) ----< (N) import_logs
core_user (1) ----< (N) export_log

core_attendancerecord (1) ----< (N) attendance_remarks

remark_reasons (1) ----< (N) attendance_remarks
```

---

## Key Indexes

### core_attendancerecord
- `idx_ep_no_date` on (ep_no, date)
- `idx_company_date` on (company_id, date)
- `idx_date` on (date)

### attendance_remarks
- `idx_ep_no_date` on (ep_no, date)
- `idx_created_by_date` on (created_by_id, created_at)
- `idx_status` on (status)
- `idx_attendance_record` on (attendance_record_id)

### remark_reasons
- `idx_company_active` on (company_id, is_active)
- `unique_company_reason` on (company_id, reason)

---

## Status Values Reference

### Attendance Status
- `P` - Present
- `A` - Absent
- `PH` - Public Holiday
- `WO` - Week Off
- `PD` - Partial Day
- `-0.5` - Half day deduction
- `-1` - Full day deduction

### Remark Status
- `pending` - Awaiting admin review
- `reviewed` - Admin has reviewed
- `resolved` - Issue resolved

### User Roles
- `root` - Full system access
- `admin` - Company-level administrator
- `user1` - Limited user with date-based access

---

## Notes

1. **Multi-tenancy**: Data is isolated by `company_id`
2. **Soft Delete**: Records are not deleted, `is_active` flag is used
3. **Audit Trail**: All tables have `created_at` and `updated_at` timestamps
4. **Foreign Keys**: All relationships use foreign keys with appropriate constraints
5. **Indexes**: Strategic indexes for performance on frequently queried columns

---

*Generated: December 17, 2025*
*System: Attendance Management System v1.0*
