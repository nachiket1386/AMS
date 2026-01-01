# 📊 Database Schema - Attendance Management System

## Overview
Your SQLite database contains **13 main tables** with **96,315 attendance records** and **37,086 mandays records**.

---

## 🏢 Core Tables

### 1. **core_company** (104 records)
Stores company information for multi-tenant data isolation.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique company ID |
| name | varchar(255) | UNIQUE, NOT NULL | Company name |
| created_at | datetime | NOT NULL | Creation timestamp |

**Relationships:**
- One-to-Many with `core_user`
- One-to-Many with `core_attendancerecord`
- One-to-Many with `core_mandaysummaryrecord`
- One-to-Many with `core_employeeassignment`
- One-to-Many with `core_accessrequest`

---

### 2. **core_user** (3 records)
Custom user model with role-based access control.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | User ID |
| username | varchar(150) | UNIQUE, NOT NULL | Username |
| password | varchar(128) | NOT NULL | Hashed password |
| email | varchar(254) | | Email address |
| role | varchar(10) | NOT NULL | Role: root/admin/user1 |
| company_id | bigint | FOREIGN KEY | Associated company |
| assigned_date_from | date | NULLABLE | Access start date (User1) |
| assigned_date_to | date | NULLABLE | Access end date (User1) |
| is_staff | bool | NOT NULL | Django admin access |
| is_active | bool | NOT NULL | Account active status |
| is_superuser | bool | NOT NULL | Superuser status |
| first_name | varchar(150) | | First name |
| last_name | varchar(150) | | Last name |
| last_login | datetime | NULLABLE | Last login timestamp |
| date_joined | datetime | NOT NULL | Account creation date |

**Roles:**
- **root**: Full system access
- **admin**: Company-level administration
- **user1**: Limited employee data access

**Relationships:**
- Many-to-One with `core_company`
- One-to-Many with `core_uploadlog`
- One-to-Many with `core_backuplog`
- One-to-Many with `core_employeeassignment`
- One-to-Many with `core_accessrequest`

---

## 📋 Attendance & Mandays Tables

### 3. **core_attendancerecord** (96,315 records)
Main attendance tracking table.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Record ID |
| ep_no | varchar(50) | NOT NULL | Employee number |
| ep_name | varchar(255) | NOT NULL | Employee name |
| company_id | bigint | FOREIGN KEY, NOT NULL | Company reference |
| date | date | NOT NULL | Attendance date |
| shift | varchar(50) | NOT NULL | Shift information |
| overstay | varchar(50) | NOT NULL | Overstay hours |
| status | varchar(10) | NOT NULL | P/A/PH/WO/-0.5/-1 |
| in_time | time | NULLABLE | First IN time |
| out_time | time | NULLABLE | First OUT time |
| in_time_2 | time | NULLABLE | Second IN time |
| out_time_2 | time | NULLABLE | Second OUT time |
| in_time_3 | time | NULLABLE | Third IN time |
| out_time_3 | time | NULLABLE | Third OUT time |
| overtime | time | NULLABLE | Overtime hours |
| overtime_to_mandays | time | NULLABLE | OT converted to mandays |
| created_at | datetime | NOT NULL | Record creation |
| updated_at | datetime | NOT NULL | Last update |

**Unique Constraint:** `(ep_no, date)` - One record per employee per day

**Indexes:**
- `ep_no, date` - Fast employee lookups
- `company_id, date` - Company-filtered queries
- `date` - Date-based filtering

**Status Values:**
- `P` - Present
- `A` - Absent
- `PH` - Public Holiday
- `WO` - Week Off
- `-0.5` - Half Day Leave
- `-1` - Full Day Leave

---

### 4. **core_mandaysummaryrecord** (37,086 records)
Mandays and overtime summary data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Record ID |
| ep_no | varchar(50) | NOT NULL | Employee number |
| company_id | bigint | FOREIGN KEY, NOT NULL | Company reference |
| punch_date | date | NOT NULL | Work date |
| mandays | decimal | NOT NULL | Mandays worked |
| ot | decimal | NOT NULL | Overtime hours (decimal) |
| regular_manday_hr | time | NOT NULL | Regular hours |
| trade | varchar(100) | NULLABLE | Trade/skill |
| contract | varchar(100) | NULLABLE | Contract type |
| plant | varchar(100) | NULLABLE | Plant code |
| plant_desc | varchar(255) | NULLABLE | Plant description |
| created_at | datetime | NOT NULL | Record creation |
| updated_at | datetime | NOT NULL | Last update |

**Unique Constraint:** `(ep_no, punch_date)` - One record per employee per day

**Indexes:**
- `ep_no, punch_date` - Fast employee lookups
- `company_id, punch_date` - Company-filtered queries
- `punch_date` - Date-based filtering

---

## 🔐 Access Control Tables

### 5. **core_employeeassignment** (1 record)
Assigns employees to User1 supervisors for data access.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Assignment ID |
| user_id | bigint | FOREIGN KEY, NOT NULL | User1 supervisor |
| ep_no | varchar(50) | NOT NULL | Employee number |
| ep_name | varchar(255) | NOT NULL | Employee name |
| company_id | bigint | FOREIGN KEY, NOT NULL | Company reference |
| access_from | date | NULLABLE | Access start (NULL=permanent) |
| access_to | date | NULLABLE | Access end (NULL=permanent) |
| assigned_by_id | bigint | FOREIGN KEY, NULLABLE | Admin who assigned |
| assigned_at | datetime | NOT NULL | Assignment timestamp |
| source | varchar(10) | NOT NULL | request/admin |
| is_active | bool | NOT NULL | Active status |

**Indexes:**
- `user_id, is_active` - Active assignments per user
- `ep_no, is_active` - Employee access lookup
- `company_id, is_active` - Company-based filtering

---

### 6. **core_accessrequest** (1 record)
User1 requests for employee data access.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Request ID |
| requester_id | bigint | FOREIGN KEY, NOT NULL | User1 making request |
| ep_no | varchar(50) | NOT NULL | Employee number |
| company_id | bigint | FOREIGN KEY, NOT NULL | Company reference |
| access_type | varchar(20) | NOT NULL | date_range/permanent |
| access_from | date | NULLABLE | Requested start date |
| access_to | date | NULLABLE | Requested end date |
| justification | TEXT | NOT NULL | Reason for access |
| status | varchar(20) | NOT NULL | pending/approved/rejected/cancelled |
| reviewed_by_id | bigint | FOREIGN KEY, NULLABLE | Admin reviewer |
| reviewed_at | datetime | NULLABLE | Review timestamp |
| rejection_reason | TEXT | | Reason if rejected |
| created_at | datetime | NOT NULL | Request creation |
| updated_at | datetime | NOT NULL | Last update |

**Status Flow:**
```
pending → approved → (creates EmployeeAssignment)
pending → rejected
pending → cancelled (by requester)
```

**Indexes:**
- `requester_id, status` - User's requests
- `status, created_at` - Pending requests queue
- `ep_no, status` - Employee-based lookup

---

### 7. **core_accessrequestauditlog** (6 records)
Audit trail for all access control actions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Log ID |
| timestamp | datetime | NOT NULL | Action timestamp |
| actor_id | bigint | FOREIGN KEY, NULLABLE | User who acted |
| action | varchar(30) | NOT NULL | Action type |
| target_user_id | bigint | FOREIGN KEY, NULLABLE | Affected User1 |
| target_ep_no | varchar(50) | | Affected employee |
| details | TEXT (JSON) | NOT NULL | Additional context |

**Action Types:**
- `request_created` - New access request
- `request_approved` - Request approved
- `request_rejected` - Request rejected
- `request_cancelled` - Request cancelled
- `assignment_created` - Manual assignment
- `assignment_removed` - Assignment deleted
- `assignment_expired` - Assignment expired

---

## 📝 Upload & Audit Tables

### 8. **core_uploadlog** (21 records)
Tracks attendance CSV uploads.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Log ID |
| user_id | bigint | FOREIGN KEY, NOT NULL | Uploader |
| uploaded_at | datetime | NOT NULL | Upload timestamp |
| filename | varchar(255) | NOT NULL | Original filename |
| success_count | INTEGER | NOT NULL | Records created |
| updated_count | INTEGER | NOT NULL | Records updated |
| error_count | INTEGER | NOT NULL | Failed records |
| error_messages | TEXT | | Error details |

---

### 9. **core_mandayuploadlog** (4 records)
Tracks mandays CSV uploads.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Log ID |
| user_id | bigint | FOREIGN KEY, NOT NULL | Uploader |
| uploaded_at | datetime | NOT NULL | Upload timestamp |
| filename | varchar(255) | NOT NULL | Original filename |
| success_count | INTEGER | NOT NULL | Records created |
| updated_count | INTEGER | NOT NULL | Records updated |
| error_count | INTEGER | NOT NULL | Failed records |
| error_messages | TEXT | | Error details |

---

### 10. **core_backuplog** (1 record)
Tracks backup and restore operations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Log ID |
| user_id | bigint | FOREIGN KEY, NOT NULL | Operator |
| operation | varchar(20) | NOT NULL | backup_full/backup_incremental/restore |
| filename | varchar(255) | NOT NULL | Backup filename |
| created_at | datetime | NOT NULL | Operation timestamp |
| companies_count | INTEGER | NOT NULL | Companies in backup |
| records_count | INTEGER | NOT NULL | Total records |
| records_added | INTEGER | NOT NULL | New records (restore) |
| records_updated | INTEGER | NOT NULL | Updated records (restore) |
| records_skipped | INTEGER | NOT NULL | Skipped records (restore) |
| success | bool | NOT NULL | Operation success |
| error_message | TEXT | | Error details |

---

## 🔗 Entity Relationship Diagram

```
┌─────────────────┐
│  core_company   │
│  (104 records)  │
└────────┬────────┘
         │
         ├──────────────────────────────────────┐
         │                                      │
         ▼                                      ▼
┌─────────────────┐                  ┌──────────────────────┐
│   core_user     │                  │ core_attendancerecord│
│  (3 records)    │                  │   (96,315 records)   │
└────────┬────────┘                  └──────────────────────┘
         │
         ├──────────────┬──────────────┬──────────────┐
         │              │              │              │
         ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│core_uploadlog│ │core_backuplog│ │core_employee │ │core_access   │
│ (21 records) │ │ (1 record)   │ │  assignment  │ │   request    │
└──────────────┘ └──────────────┘ │ (1 record)   │ │ (1 record)   │
                                  └──────────────┘ └──────┬───────┘
                                                          │
                                                          ▼
                                                  ┌──────────────────┐
                                                  │core_accessrequest│
                                                  │    auditlog      │
                                                  │  (6 records)     │
                                                  └──────────────────┘

┌─────────────────┐
│  core_company   │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│core_mandaysummaryrecord  │
│    (37,086 records)      │
└──────────────────────────┘
         │
         ▼
┌──────────────────────────┐
│  core_mandayuploadlog    │
│     (4 records)          │
└──────────────────────────┘
```

---

## 📊 Database Statistics

| Table | Records | Purpose |
|-------|---------|---------|
| core_attendancerecord | 96,315 | Daily attendance tracking |
| core_mandaysummaryrecord | 37,086 | Mandays & overtime summary |
| core_company | 104 | Company master data |
| core_uploadlog | 21 | Attendance upload history |
| core_accessrequestauditlog | 6 | Access control audit trail |
| core_mandayuploadlog | 4 | Mandays upload history |
| core_user | 3 | System users |
| core_accessrequest | 1 | Pending/processed requests |
| core_employeeassignment | 1 | Active assignments |
| core_backuplog | 1 | Backup operations |

**Total Records:** ~133,438 records

---

## 🔍 Key Features

### Multi-Tenancy
- All data isolated by `company_id`
- Users assigned to specific companies
- Company-level access control

### Role-Based Access Control (RBAC)
- **Root**: Full system access
- **Admin**: Company-level management
- **User1**: Limited employee access via assignments

### Audit Trail
- All uploads logged with success/error counts
- Access requests tracked through lifecycle
- Assignment changes recorded in audit log

### Data Integrity
- Unique constraints prevent duplicate records
- Foreign keys maintain referential integrity
- Indexes optimize query performance

### Flexible Access Control
- Date-range based access for User1
- Permanent or temporary assignments
- Request-approval workflow for access

---

## 🎯 Performance Optimizations

### Indexes Created
1. **Attendance Records**: `(ep_no, date)`, `(company_id, date)`, `(date)`
2. **Mandays Records**: `(ep_no, punch_date)`, `(company_id, punch_date)`, `(punch_date)`
3. **Access Requests**: `(requester_id, status)`, `(status, created_at)`, `(ep_no, status)`
4. **Employee Assignments**: `(user_id, is_active)`, `(ep_no, is_active)`, `(company_id, is_active)`
5. **Audit Logs**: `(timestamp)`, `(actor_id, timestamp)`, `(target_user_id, timestamp)`

These indexes ensure fast queries for:
- Employee attendance lookups
- Date-range filtering
- Company-based data isolation
- Access control checks
- Audit trail searches
