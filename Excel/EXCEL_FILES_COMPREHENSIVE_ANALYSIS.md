# Excel Files Comprehensive Analysis for Web Application Integration

## Executive Summary

You have **6 Excel files** in the Excel folder that contain attendance and workforce management data. **5 files are readable** (HTML format), and **1 file is corrupted** (CrystalReportViewer1.xlsx).

### Key Findings:
- **All files share common employee and contractor information fields**
- **Strong data relationships exist between files** - they can be linked via EP NO, Contractor Code, Punch Date
- **Total Records: 41,502 rows** across all readable files
- **Data covers December 2025** (dates from 01/12/2025 to 13/12/2025)

---

## File-by-File Analysis

### 1. **Date wise ARC Summary (1).xls** ✅
**Purpose:** Daily attendance summary with mandays and overtime tracking

**Size:** 15,496 rows × 19 columns

**Key Columns:**
- Employee Info: `epNo`, `punchDate`
- Contractor Info: `contCode`, `contract`
- Work Details: `trade`, `skill`, `activityType`
- Location: `plant`, `sector`, `siteCode`, `plantDesc`
- Time Tracking: `mandays`, `regularMandayHr`, `ot` (overtime)

**Data Quality:**
- ✅ No nulls in critical fields (epNo, punchDate, contCode)
- ⚠️ 94% missing data in `locationStatus` (14,547 nulls)

**Unique Values:**
- 1,192 unique employees
- 10 contractors
- 13 days of data
- 29 different trades

**Sample Data Pattern:**
```
EP: PP5000014534 | Date: 01/12/2025 | Contractor: 118378
Trade: HSC OPERATOR-8HR | Mandays: 1.0 | OT: 0.0
```

---

### 2. **OVERTIME (2).xls** ✅
**Purpose:** Overtime request and approval tracking

**Size:** 770 rows × 30 columns

**Key Columns:**
- Employee Info: `EP NO`, `EP NAME`, `PUNCHDATE`
- Contractor Info: `CONTRACTOR CODE`, `CONTRACTOR NAME`
- Location: `SECTOR NAME`, `PLANT NAME`, `AREA OF MOVEMENT`
- Time Details: `ACTUAL OVERSTAY`, `REQUESTED OVERTIME`, `APPROVED OVERTIME`
- Approval Workflow: `CONTRACTOR OT REQUEST DATE`, `EIC APPROVE/REJECT DATE`, `OT REQUEST STATUS`
- Approvers: `ACTUAL EIC CODE`, `REQUESTED EIC CODE`, `ADMIN AUTHORIZED BY`

**Data Quality:**
- ✅ All employee and contractor fields complete
- ⚠️ 64% missing approved overtime (494 nulls) - indicates pending requests
- ⚠️ 100% missing admin fields (not yet processed)

**Unique Values:**
- 252 unique employees
- 7 contractors
- 12 days of data
- 3 status types: Approved, Pending, Rejected

**Approval Status Distribution:**
- Approved: ~36% (277 records)
- Pending: ~64% (493 records)

**Sample Data Pattern:**
```
EP: PP5001002335 | Date: 01/12/2025
Actual Overstay: 08:02 | Requested OT: 00:00 | Approved OT: 00:00
Status: Approved | EIC: Subhash Jolotia
```

---

### 3. **PARTIAL DAY.xls** ✅
**Purpose:** Partial day work requests (employees working less than full shift)

**Size:** 19 rows × 26 columns

**Key Columns:**
- Employee Info: `EP NO`, `EP NAME`, `PUNCHDATE`
- Contractor Info: `CONTRACTOR CODE`, `CONTRACTOR NAME`
- Time Details: `ACTUAL PD HOURS`, `REQUESTED PD HOURS`, `APPROVED PD HOURS`
- Conversion: `MANDAY CONVERSION` (e.g., 6 hours = 0.75 mandays)
- Approval: `CONTRACTOR PD REQUEST DATE`, `EIC APPROVE/REJECT DATE`, `PD REQUEST STATUS`

**Data Quality:**
- ✅ All employee fields complete
- ⚠️ 26% missing approved hours (5 nulls) - pending requests
- ⚠️ 100% missing EIC NAME fields

**Unique Values:**
- 16 unique employees
- 3 contractors
- 9 days of data
- 6 different manday conversion values (0.0, 0.5, 0.75, etc.)

**Manday Conversion Logic:**
- 4 hours = 0.5 mandays
- 6 hours = 0.75 mandays
- 7.5 hours = varies

**Sample Data Pattern:**
```
EP: PP5003001178 | Date: 01/12/2025
Actual: 06:01 | Requested: 06:00 | Approved: 06:00
Manday Conversion: 0.75 | Status: Approved
```

---

### 4. **Punchrecord Report (6).xls** ✅
**Purpose:** Detailed punch-in/punch-out records for all employees

**Size:** 25,071 rows × 29 columns (LARGEST FILE)

**Key Columns:**
- Employee Info: `EP NO`, `EP NAME`, `PUNCHDATE`
- Contractor Info: `CONTRACTOR CODE`, `CONTRACTOR NAME`
- Location: `SECTOR NAME`, `PLANT NAME`, `AREA OF MOVEMENT`
- Shift: `SHIFT` (e.g., "A (06:00-14:00)", "B (14:00-22:00)", "C (22:00-06:00)")
- Punch Times: `PUNCH1 IN`, `PUNCH2 OUT`, `PUNCH3 IN`, `PUNCH4 OUT`, `PUNCH5 IN`, `PUNCH6 OUT`
- Time Calculations: `EARLY IN`, `LATE COME`, `EARLY OUT`, `HOURS WORKED`, `OVERSTAY`, `OVERTIME`
- Status: `STATUS` (P=Present, A=Absent, etc.)
- Manual: `REGULAR HOURS`, `MANUAL REQUEST`

**Data Quality:**
- ✅ All employee and contractor fields complete
- ⚠️ 63% missing AREA OF MOVEMENT (15,691 nulls)
- ⚠️ 97% missing PUNCH3-6 (most employees have only 2 punches)
- ⚠️ 99% missing OVERTIME field (24,795 nulls)
- ⚠️ 99% missing MANUAL REQUEST (24,969 nulls)

**Unique Values:**
- 2,399 unique employees (MOST COMPREHENSIVE)
- 42 contractors
- 13 days of data
- 58 different trades
- 10 different shifts
- 5 status types

**Shift Patterns:**
- A (06:00-14:00) - Morning
- B (14:00-22:00) - Afternoon
- C (22:00-06:00) - Night

**Sample Data Pattern:**
```
EP: PP5000014534 | Date: 01/12/2025 | Shift: C (22:00-06:00)
Punch In: 22:01 | Punch Out: 06:04 (N)
Late Come: 00:01 | Hours Worked: 08:03 | Overstay: 00:04
Status: P (Present)
```

---

### 5. **Regularization Audit Report (1).xls** ✅
**Purpose:** Punch time correction/regularization requests

**Size:** 146 rows × 29 columns

**Key Columns:**
- Employee Info: `EP NO`, `EP NAME`, `PUNCHDATE`
- Contractor Info: `CONTRACTOR CODE`, `CONTRACTOR NAME`
- Old vs New Times: `OLD PUNCH IN`, `OLD PUNCH OUT`, `NEW PUNCH IN`, `NEW PUNCH OUT`
- Request Details: `CONTRACTOR REQUEST DATE`, `CONTRACTOR REMARKS`, `CONTRACTOR REASON`
- Approval: `EIC APPROVE/REJECT DATE`, `EIC REQUEST REMARKS`, `REQUEST STATUS`
- Approvers: `ACTUAL EIC CODE`, `REQUESTED EIC CODE`, `ADMIN AUTHORIZED BY`

**Data Quality:**
- ✅ All employee and contractor fields complete
- ⚠️ 14% missing old punch times (21 nulls in OLD PUNCH IN)
- ⚠️ 32% missing EIC approval data (46 nulls) - pending requests
- ⚠️ 100% missing admin fields (not yet processed)

**Unique Values:**
- 103 unique employees
- 9 contractors
- 12 days of data
- 71 different reasons for regularization

**Common Reasons:**
- "Late Coming"
- "BUS LATE"
- "Shift Not Available in System"
- "Vegetable Purchase in city"

**Status Distribution:**
- Approved: ~68% (100 records)
- Pending: ~32% (46 records)

**Sample Data Pattern:**
```
EP: PP5001504036 | Date: 01/12/2025
Old: 14:13 to 06:01 | New: 14:00 to 22:00
Reason: BUS LATE | Status: Approved
```

---

### 6. **CrystalReportViewer1.xlsx** ❌
**Status:** CORRUPTED - Cannot be read

**Error:** "Unable to read workbook: could not read stylesheet. Invalid XML."

**Recommendation:** 
- Request a fresh export from the source system
- Or convert to CSV format
- Or repair using Excel's built-in repair tool

---

## Common Fields Across All Files (Data Relationships)

### Primary Keys for Linking:
1. **EP NO** (Employee ID) - Present in ALL files
2. **PUNCHDATE** - Present in ALL files
3. **CONTRACTOR CODE** - Present in ALL files

### Shared Fields:
| Field | File 1 | File 2 | File 3 | File 4 | File 5 |
|-------|--------|--------|--------|--------|--------|
| EP NO | ✅ | ✅ | ✅ | ✅ | ✅ |
| EP NAME | ❌ | ✅ | ✅ | ✅ | ✅ |
| PUNCHDATE | ✅ | ✅ | ✅ | ✅ | ✅ |
| CONTRACTOR CODE | ✅ | ✅ | ✅ | ✅ | ✅ |
| CONTRACTOR NAME | ❌ | ✅ | ✅ | ✅ | ✅ |
| SECTOR NAME | ✅ | ✅ | ✅ | ✅ | ✅ |
| PLANT NAME | ✅ | ✅ | ✅ | ✅ | ✅ |
| TRADE NAME | ✅ | ✅ | ✅ | ✅ | ✅ |
| SKILL | ✅ | ✅ | ✅ | ✅ | ✅ |
| SHIFT | ❌ | ✅ | ✅ | ✅ | ✅ |

**Legend:**
- File 1: Date wise ARC Summary
- File 2: OVERTIME
- File 3: PARTIAL DAY
- File 4: Punchrecord Report
- File 5: Regularization Audit Report

---

## Data Similarities & Relationships

### 🔗 **Strong Relationships:**

1. **Master-Detail Relationship:**
   - **Punchrecord Report** = Master (most detailed, 25K records)
   - **Date wise ARC Summary** = Aggregated summary (15K records)
   - **OVERTIME** = Exception records (770 records)
   - **PARTIAL DAY** = Exception records (19 records)
   - **Regularization** = Correction records (146 records)

2. **Data Flow:**
   ```
   Punchrecord Report (Raw Punches)
         ↓
   Date wise ARC Summary (Daily Aggregation)
         ↓
   OVERTIME / PARTIAL DAY / Regularization (Exceptions & Corrections)
   ```

3. **Linking Example:**
   ```sql
   -- You can join all files using:
   SELECT *
   FROM punchrecord p
   LEFT JOIN arc_summary a ON p.ep_no = a.epNo AND p.punchdate = a.punchDate
   LEFT JOIN overtime o ON p.ep_no = o.ep_no AND p.punchdate = o.punchdate
   LEFT JOIN partial_day pd ON p.ep_no = pd.ep_no AND p.punchdate = pd.punchdate
   LEFT JOIN regularization r ON p.ep_no = r.ep_no AND p.punchdate = r.punchdate
   ```

---

## Database Schema Recommendation

### Proposed Tables:

#### 1. **employees** (Master Table)
```sql
- ep_no (PK)
- ep_name
- contractor_code (FK)
- sector_name
- plant_name
- department_name
- trade_name
- skill
- card_category
```

#### 2. **contractors** (Master Table)
```sql
- contractor_code (PK)
- contractor_name
```

#### 3. **punch_records** (Transaction Table)
```sql
- id (PK)
- ep_no (FK)
- punchdate
- shift
- punch1_in, punch2_out, punch3_in, punch4_out, punch5_in, punch6_out
- early_in, late_come, early_out
- hours_worked, overstay, overtime
- status
- regular_hours
- manual_request
```

#### 4. **daily_summary** (Aggregated Table)
```sql
- id (PK)
- ep_no (FK)
- punchdate
- mandays
- regular_manday_hr
- ot
- location_status
```

#### 5. **overtime_requests** (Transaction Table)
```sql
- id (PK)
- ep_no (FK)
- punchdate
- actual_overstay
- requested_overtime, approved_overtime
- requested_regular_hours, approved_regular_hours
- contractor_request_date, contractor_remarks, contractor_reason
- actual_eic_code, requested_eic_code
- eic_approve_date, eic_remarks
- admin_authorized_by, admin_remarks
- status (Pending/Approved/Rejected)
```

#### 6. **partial_day_requests** (Transaction Table)
```sql
- id (PK)
- ep_no (FK)
- punchdate
- actual_pd_hours, requested_pd_hours, approved_pd_hours
- manday_conversion
- contractor_request_date, contractor_remarks
- eic_code, eic_approve_date, eic_remarks
- status
```

#### 7. **regularization_requests** (Transaction Table)
```sql
- id (PK)
- ep_no (FK)
- punchdate
- old_punch_in, old_punch_out
- new_punch_in, new_punch_out
- contractor_request_date, contractor_remarks, contractor_reason
- eic_code, eic_approve_date, eic_remarks
- admin_authorized_by, admin_remarks
- status
```

---

## Web Application Integration Strategy

### Phase 1: Data Import
1. **Create upload interface** for each file type
2. **Validate data** before import (check EP NO format, date format, etc.)
3. **Handle duplicates** (use EP NO + PUNCHDATE as composite key)
4. **Log import errors** for review

### Phase 2: User-Based Data Display
Based on user role, show different views:

#### **For Employees:**
- My attendance summary (from daily_summary)
- My punch records (from punch_records)
- My pending requests (overtime, partial day, regularization)

#### **For Contractors:**
- All employees under their contractor code
- Pending approval requests
- Summary reports by date range

#### **For EIC (Engineer-in-Charge):**
- Approval dashboard for overtime/partial day/regularization
- Team attendance overview
- Exception reports

#### **For Admins:**
- System-wide reports
- Data upload interface
- User management

### Phase 3: Features to Build

1. **File Upload Module:**
   - Drag-and-drop Excel upload
   - Auto-detect file type based on columns
   - Preview before import
   - Validation and error reporting

2. **Dashboard:**
   - Today's attendance summary
   - Pending approvals count
   - Recent activities

3. **Reports:**
   - Daily attendance report
   - Overtime summary by contractor
   - Regularization audit trail
   - Partial day analysis

4. **Approval Workflow:**
   - Contractor submits request
   - EIC approves/rejects
   - Admin final authorization
   - Email notifications

5. **Search & Filter:**
   - By EP NO, name, contractor, date range
   - By status (Pending/Approved/Rejected)
   - By plant, sector, trade

---

## Data Quality Issues to Address

### Critical Issues:
1. ⚠️ **Missing EIC Names** in Partial Day file (100% null)
2. ⚠️ **Missing Admin fields** in Overtime and Regularization (100% null)
3. ⚠️ **Inconsistent column naming** (epNo vs EP NO)
4. ⚠️ **Date format inconsistency** (DD/MM/YYYY vs timestamps)

### Recommendations:
1. **Standardize column names** during import
2. **Convert all dates** to ISO format (YYYY-MM-DD)
3. **Handle null values** with default values or validation
4. **Add data validation rules** in upload interface

---

## Next Steps

1. ✅ **Create database schema** based on recommendations above
2. ✅ **Build file upload interface** with validation
3. ✅ **Implement data import logic** with error handling
4. ✅ **Create user authentication** and role-based access
5. ✅ **Build dashboards** for each user type
6. ✅ **Implement approval workflows**
7. ✅ **Add reporting features**

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Files | 6 |
| Readable Files | 5 |
| Total Records | 41,502 |
| Unique Employees | 2,399 |
| Unique Contractors | 42 |
| Date Range | 01/12/2025 - 13/12/2025 |
| Largest File | Punchrecord Report (25,071 rows) |
| Smallest File | Partial Day (19 rows) |

---

**Generated:** December 2025
**Analysis Tool:** Python + Pandas
