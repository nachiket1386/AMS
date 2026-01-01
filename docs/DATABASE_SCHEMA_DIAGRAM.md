# 📊 Excel Upload System - Database Schema

## Complete Database Structure

This document shows all database tables and their columns for the Excel File Upload system.

---

## 🗂️ Master Tables (Reference Data)

### 1. **employees** (Employee Master)
```
┌─────────────────────────────────────────┐
│           EMPLOYEES TABLE               │
├─────────────────────────────────────────┤
│ 🔑 ep_no (PK)          VARCHAR(12)     │
│    ep_name             VARCHAR(255)     │
│ 🔗 contractor_id (FK)  INTEGER          │
│    sector_name         VARCHAR(100)     │
│    plant_name          VARCHAR(100)     │
│    department_name     VARCHAR(100)     │
│    trade_name          VARCHAR(100)     │
│    skill               VARCHAR(50)      │
│    card_category       VARCHAR(50)      │
│    created_at          DATETIME         │
│    updated_at          DATETIME         │
└─────────────────────────────────────────┘
```
**Purpose:** Stores employee master data  
**Primary Key:** ep_no (Employee Number)  
**Foreign Keys:** contractor_id → contractors

---

### 2. **contractors** (Contractor Master)
```
┌─────────────────────────────────────────┐
│         CONTRACTORS TABLE               │
├─────────────────────────────────────────┤
│ 🔑 contractor_code (PK) INTEGER         │
│    contractor_name      VARCHAR(255)    │
│    created_at           DATETIME        │
│    updated_at           DATETIME        │
└─────────────────────────────────────────┘
```
**Purpose:** Stores contractor master data  
**Primary Key:** contractor_code

---

### 3. **plants** (Plant Master)
```
┌─────────────────────────────────────────┐
│            PLANTS TABLE                 │
├─────────────────────────────────────────┤
│ 🔑 plant_code (PK)     VARCHAR(50)     │
│    plant_name          VARCHAR(255)     │
│    sector_name         VARCHAR(100)     │
│    site_code           VARCHAR(50)      │
│    site_desc           VARCHAR(255)     │
│    created_at          DATETIME         │
└─────────────────────────────────────────┘
```
**Purpose:** Stores plant/location master data  
**Primary Key:** plant_code

---

## 📝 Transaction Tables (Daily Data)

### 4. **punch_records** (Punchrecord File Data)
```
┌─────────────────────────────────────────┐
│         PUNCH_RECORDS TABLE             │
├─────────────────────────────────────────┤
│ 🔑 id (PK)             INTEGER          │
│ 🔗 employee_id (FK)    VARCHAR(12)      │
│    punchdate           DATE             │
│    shift               VARCHAR(50)      │
│    punch1_in           TIME             │
│    punch2_out          TIME             │
│    punch3_in           TIME             │
│    punch4_out          TIME             │
│    punch5_in           TIME             │
│    punch6_out          TIME             │
│    early_in            TIME             │
│    late_come           TIME             │
│    early_out           TIME             │
│    hours_worked        TIME             │
│    overstay            TIME             │
│    overtime            TIME             │
│    status              VARCHAR(10)      │
│    regular_hours       TIME             │
│    manual_request      BOOLEAN          │
│    created_at          DATETIME         │
└─────────────────────────────────────────┘
```
**Purpose:** Stores punch in/out records from Punchrecord files  
**Primary Key:** id  
**Foreign Keys:** employee_id → employees  
**Unique:** (employee_id, punchdate)

---

### 5. **daily_summary** (ARC Summary File Data)
```
┌─────────────────────────────────────────┐
│        DAILY_SUMMARY TABLE              │
├─────────────────────────────────────────┤
│ 🔑 id (PK)             INTEGER          │
│ 🔗 employee_id (FK)    VARCHAR(12)      │
│    punchdate           DATE             │
│    mandays             DECIMAL(5,2)     │
│    regular_manday_hr   TIME             │
│    ot                  DECIMAL(5,2)     │
│    location_status     VARCHAR(50)      │
│    created_at          DATETIME         │
└─────────────────────────────────────────┘
```
**Purpose:** Stores daily attendance summary from ARC Summary files  
**Primary Key:** id  
**Foreign Keys:** employee_id → employees  
**Unique:** (employee_id, punchdate)

---

### 6. **overtime_requests** (Overtime File Data)
```
┌─────────────────────────────────────────┐
│      OVERTIME_REQUESTS TABLE            │
├─────────────────────────────────────────┤
│ 🔑 id (PK)                  INTEGER     │
│ 🔗 employee_id (FK)         VARCHAR(12) │
│    punchdate                DATE        │
│    actual_overstay          TIME        │
│    requested_overtime       TIME        │
│    approved_overtime        TIME        │
│    requested_regular_hours  TIME        │
│    approved_regular_hours   TIME        │
│    contractor_request_date  DATETIME    │
│    contractor_remarks       TEXT        │
│    contractor_reason        TEXT        │
│    actual_eic_code          INTEGER     │
│    requested_eic_code       INTEGER     │
│    eic_approve_date         DATETIME    │
│    eic_remarks              TEXT        │
│    status                   VARCHAR(20) │
│    created_at               DATETIME    │
└─────────────────────────────────────────┘
```
**Purpose:** Stores overtime requests from Overtime files  
**Primary Key:** id  
**Foreign Keys:** employee_id → employees  
**Unique:** (employee_id, punchdate)  
**Status Values:** Pending, Approved, Rejected

---

### 7. **partial_day_requests** (Partial Day File Data)
```
┌─────────────────────────────────────────┐
│    PARTIAL_DAY_REQUESTS TABLE           │
├─────────────────────────────────────────┤
│ 🔑 id (PK)                 INTEGER      │
│ 🔗 employee_id (FK)        VARCHAR(12)  │
│    punchdate               DATE         │
│    actual_pd_hours         TIME         │
│    requested_pd_hours      TIME         │
│    approved_pd_hours       TIME         │
│    manday_conversion       DECIMAL(3,2) │
│    contractor_request_date DATETIME     │
│    contractor_remarks      TEXT         │
│    eic_code                INTEGER      │
│    eic_approve_date        DATETIME     │
│    eic_remarks             TEXT         │
│    status                  VARCHAR(20)  │
│    created_at              DATETIME     │
└─────────────────────────────────────────┘
```
**Purpose:** Stores partial day requests from Partial Day files  
**Primary Key:** id  
**Foreign Keys:** employee_id → employees  
**Unique:** (employee_id, punchdate)  
**Status Values:** Pending, Approved, Rejected

---

### 8. **regularization_requests** (Regularization File Data)
```
┌─────────────────────────────────────────┐
│   REGULARIZATION_REQUESTS TABLE         │
├─────────────────────────────────────────┤
│ 🔑 id (PK)                 INTEGER      │
│ 🔗 employee_id (FK)        VARCHAR(12)  │
│    punchdate               DATE         │
│    old_punch_in            TIME         │
│    old_punch_out           TIME         │
│    new_punch_in            TIME         │
│    new_punch_out           TIME         │
│    contractor_request_date DATETIME     │
│    contractor_remarks      TEXT         │
│    contractor_reason       TEXT         │
│    eic_code                INTEGER      │
│    eic_approve_date        DATETIME     │
│    eic_remarks             TEXT         │
│    status                  VARCHAR(20)  │
│    created_at              DATETIME     │
└─────────────────────────────────────────┘
```
**Purpose:** Stores regularization requests from Regularization files  
**Primary Key:** id  
**Foreign Keys:** employee_id → employees  
**Unique:** (employee_id, punchdate)  
**Status Values:** Pending, Approved, Rejected

---

## 📋 Audit & Log Tables

### 9. **import_logs** (Import History)
```
┌─────────────────────────────────────────┐
│          IMPORT_LOGS TABLE              │
├─────────────────────────────────────────┤
│ 🔑 id (PK)             INTEGER          │
│ 🔗 user_id (FK)        INTEGER          │
│    filename            VARCHAR(255)     │
│    file_type           VARCHAR(50)      │
│    total_rows          INTEGER          │
│    imported_rows       INTEGER          │
│    duplicate_rows      INTEGER          │
│    error_rows          INTEGER          │
│    status              VARCHAR(20)      │
│    error_report_path   VARCHAR(500)     │
│    created_at          DATETIME         │
└─────────────────────────────────────────┘
```
**Purpose:** Tracks all Excel file imports  
**Primary Key:** id  
**Foreign Keys:** user_id → auth_user

---

### 10. **export_logs** (Export History)
```
┌─────────────────────────────────────────┐
│          EXPORT_LOGS TABLE              │
├─────────────────────────────────────────┤
│ 🔑 id (PK)             INTEGER          │
│ 🔗 user_id (FK)        INTEGER          │
│    export_type         VARCHAR(50)      │
│    record_count        INTEGER          │
│    filters             JSON             │
│    created_at          DATETIME         │
└─────────────────────────────────────────┘
```
**Purpose:** Tracks all data exports  
**Primary Key:** id  
**Foreign Keys:** user_id → auth_user

---

### 11. **upload_permissions** (User Permissions)
```
┌─────────────────────────────────────────┐
│      UPLOAD_PERMISSIONS TABLE           │
├─────────────────────────────────────────┤
│ 🔑 id (PK)             INTEGER          │
│ 🔗 user_id (FK)        INTEGER          │
│    file_type           VARCHAR(50)      │
│    can_upload          BOOLEAN          │
│ 🔗 granted_by_id (FK)  INTEGER          │
│    granted_at          DATETIME         │
└─────────────────────────────────────────┘
```
**Purpose:** Manages user upload permissions  
**Primary Key:** id  
**Foreign Keys:** user_id → auth_user, granted_by_id → auth_user  
**Unique:** (user_id, file_type)

---

## 🔗 Relationships Diagram

```
┌──────────────┐
│ contractors  │
└──────┬───────┘
       │
       │ 1:N
       │
       ▼
┌──────────────┐         ┌─────────────────┐
│  employees   │◄────────│  punch_records  │
└──────┬───────┘    N:1  └─────────────────┘
       │
       │ 1:N
       ├──────────────────┬──────────────────┬──────────────────┐
       │                  │                  │                  │
       ▼                  ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│daily_summary │  │overtime_req  │  │partial_day   │  │regularization│
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘


┌──────────────┐
│  auth_user   │
└──────┬───────┘
       │
       │ 1:N
       ├──────────────────┬──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ import_logs  │  │ export_logs  │  │upload_perms  │
└──────────────┘  └──────────────┘  └──────────────┘


┌──────────────┐
│   plants     │  (Independent reference table)
└──────────────┘
```

---

## 📊 File Type to Table Mapping

| Excel File Type | Database Table | Purpose |
|----------------|----------------|---------|
| **🕐 Punchrecord** | `punch_records` | Employee punch in/out times |
| **📊 ARC Summary** | `daily_summary` | Daily attendance summary |
| **⏰ Overtime** | `overtime_requests` | Overtime requests & approvals |
| **📅 Partial Day** | `partial_day_requests` | Partial day attendance |
| **✏️ Regularization** | `regularization_requests` | Attendance corrections |
| **Master Data** | `employees`, `contractors`, `plants` | Reference data |

---

## 🔍 Key Indexes

### Performance Indexes:
- **employees:** contractor, plant_name, sector_name
- **punch_records:** punchdate, (employee, punchdate), status
- **daily_summary:** punchdate, (employee, punchdate)
- **overtime_requests:** punchdate, (employee, punchdate), status
- **partial_day_requests:** punchdate, (employee, punchdate), status
- **regularization_requests:** punchdate, (employee, punchdate), status
- **import_logs:** (user, created_at), created_at, file_type
- **export_logs:** (user, created_at), created_at

---

## 📝 Column Naming Convention

### Common Patterns:
- **Primary Keys:** `id` (auto-increment) or specific code (e.g., `ep_no`, `contractor_code`)
- **Foreign Keys:** `{table}_id` (e.g., `employee_id`, `user_id`)
- **Timestamps:** `created_at`, `updated_at`, `granted_at`
- **Status Fields:** `status` (with predefined choices)
- **Date Fields:** `punchdate`, `{action}_date`
- **Time Fields:** `punch1_in`, `punch2_out`, etc.

---

## 💾 Data Types Summary

| Type | Usage | Example Columns |
|------|-------|----------------|
| **VARCHAR** | Text fields | ep_name, contractor_name, status |
| **INTEGER** | Whole numbers | id, contractor_code, eic_code |
| **DATE** | Date only | punchdate |
| **TIME** | Time only | punch1_in, hours_worked |
| **DATETIME** | Date + Time | created_at, contractor_request_date |
| **DECIMAL** | Precise numbers | mandays, ot, manday_conversion |
| **BOOLEAN** | True/False | can_upload, manual_request |
| **TEXT** | Long text | remarks, reason |
| **JSON** | Structured data | filters |

---

## 🎯 Quick Reference

### Total Tables: **11**
- **Master Tables:** 3 (employees, contractors, plants)
- **Transaction Tables:** 5 (punch_records, daily_summary, overtime_requests, partial_day_requests, regularization_requests)
- **Audit Tables:** 3 (import_logs, export_logs, upload_permissions)

### Key Features:
✅ Foreign key relationships for data integrity  
✅ Unique constraints to prevent duplicates  
✅ Indexes for fast queries  
✅ Audit trails for all imports/exports  
✅ Permission management  
✅ Status tracking for requests  

---

## 📖 Usage Examples

### Query Punch Records:
```sql
SELECT e.ep_no, e.ep_name, pr.punchdate, pr.punch1_in, pr.punch2_out
FROM punch_records pr
JOIN employees e ON pr.employee_id = e.ep_no
WHERE pr.punchdate = '2024-01-15';
```

### Query Import History:
```sql
SELECT filename, file_type, imported_rows, error_rows, created_at
FROM import_logs
WHERE user_id = 1
ORDER BY created_at DESC;
```

### Query Employee with Contractor:
```sql
SELECT e.ep_no, e.ep_name, c.contractor_name
FROM employees e
JOIN contractors c ON e.contractor_id = c.contractor_code;
```

---

**This schema supports all 5 Excel file types and provides complete audit trails for all operations!** 🎉
