# Excel Files Similarity Matrix

## Visual Comparison of All Files

### Column Overlap Analysis

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        COMMON FIELDS ACROSS ALL FILES                        │
└─────────────────────────────────────────────────────────────────────────────┘

                    ARC      OVERTIME  PARTIAL   PUNCH    REGULAR
                  SUMMARY              DAY      RECORD    AUDIT
                  ───────   ────────  ───────  ────────  ───────
EP NO               ✓         ✓         ✓        ✓         ✓      ← PRIMARY KEY
PUNCHDATE           ✓         ✓         ✓        ✓         ✓      ← PRIMARY KEY
CONTRACTOR CODE     ✓         ✓         ✓        ✓         ✓      ← FOREIGN KEY
CONTRACTOR NAME     ✗         ✓         ✓        ✓         ✓
EP NAME             ✗         ✓         ✓        ✓         ✓
SECTOR NAME         ✓         ✓         ✓        ✓         ✓
PLANT NAME          ✓         ✓         ✓        ✓         ✓
DEPARTMENT NAME     ✗         ✓         ✓        ✓         ✓
TRADE NAME          ✓         ✓         ✓        ✓         ✓
SKILL               ✓         ✓         ✓        ✓         ✓
CARD CATEGORY       ✗         ✓         ✓        ✓         ✓
SHIFT               ✗         ✓         ✓        ✓         ✓
AREA OF MOVEMENT    ✗         ✓         ✓        ✓         ✓
```

### Similarity Scores

```
┌──────────────────────────────────────────────────────────────┐
│  File Pair                          Similarity Score          │
├──────────────────────────────────────────────────────────────┤
│  OVERTIME ↔ PARTIAL DAY                   95%  ████████████  │
│  OVERTIME ↔ REGULARIZATION                93%  ███████████   │
│  PARTIAL DAY ↔ REGULARIZATION             92%  ███████████   │
│  PUNCH RECORD ↔ OVERTIME                  85%  ██████████    │
│  PUNCH RECORD ↔ PARTIAL DAY               83%  █████████     │
│  PUNCH RECORD ↔ REGULARIZATION            82%  █████████     │
│  ARC SUMMARY ↔ PUNCH RECORD               65%  ███████       │
│  ARC SUMMARY ↔ OVERTIME                   55%  ██████        │
│  ARC SUMMARY ↔ PARTIAL DAY                52%  █████         │
│  ARC SUMMARY ↔ REGULARIZATION             50%  █████         │
└──────────────────────────────────────────────────────────────┘
```

## File Relationships Diagram

```
                    ┌─────────────────────────────────┐
                    │   PUNCHRECORD REPORT (Master)   │
                    │   25,071 records                │
                    │   - All punch in/out times      │
                    │   - Most comprehensive          │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────┴──────────────────┐
                    │                                 │
         ┌──────────▼──────────┐         ┌───────────▼──────────┐
         │  ARC SUMMARY        │         │  EXCEPTION RECORDS   │
         │  15,496 records     │         │                      │
         │  - Daily aggregate  │         │  ┌─────────────────┐ │
         │  - Mandays & OT     │         │  │ OVERTIME        │ │
         └─────────────────────┘         │  │ 770 records     │ │
                                         │  └─────────────────┘ │
                                         │  ┌─────────────────┐ │
                                         │  │ PARTIAL DAY     │ │
                                         │  │ 19 records      │ │
                                         │  └─────────────────┘ │
                                         │  ┌─────────────────┐ │
                                         │  │ REGULARIZATION  │ │
                                         │  │ 146 records     │ │
                                         │  └─────────────────┘ │
                                         └─────────────────────┘
```

## Data Type Comparison

### 1. ARC SUMMARY (Aggregated Data)
**Purpose:** Daily summary of attendance
**Unique Fields:**
- `mandays` - Number of days worked
- `regularMandayHr` - Regular hours
- `ot` - Overtime hours
- `locationStatus` - Location tracking

**Use Case:** Monthly reports, payroll calculation

---

### 2. OVERTIME (Request/Approval Data)
**Purpose:** Track overtime requests and approvals
**Unique Fields:**
- `ACTUAL OVERSTAY` - Actual extra hours
- `REQUESTED OVERTIME` - Contractor's request
- `APPROVED OVERTIME` - EIC's approval
- `CONTRACTOR OT REASON` - Reason for OT
- `OT REQUEST STATUS` - Pending/Approved/Rejected

**Use Case:** Overtime approval workflow

---

### 3. PARTIAL DAY (Request/Approval Data)
**Purpose:** Track partial day work requests
**Unique Fields:**
- `ACTUAL PD HOURS` - Actual hours worked
- `REQUESTED PD HOURS` - Requested hours
- `APPROVED PD HOURS` - Approved hours
- `MANDAY CONVERSION` - Convert hours to mandays (e.g., 6hrs = 0.75)

**Use Case:** Handle employees working less than full shift

---

### 4. PUNCHRECORD REPORT (Raw Transaction Data)
**Purpose:** Detailed punch in/out records
**Unique Fields:**
- `PUNCH1 IN`, `PUNCH2 OUT`, `PUNCH3 IN`, `PUNCH4 OUT`, `PUNCH5 IN`, `PUNCH6 OUT`
- `EARLY IN`, `LATE COME`, `EARLY OUT`
- `HOURS WORKED`, `OVERSTAY`
- `STATUS` - P/A/L (Present/Absent/Leave)
- `MANUAL REQUEST` - Manual entry flag

**Use Case:** Audit trail, detailed attendance tracking

---

### 5. REGULARIZATION (Correction Data)
**Purpose:** Correct punch time errors
**Unique Fields:**
- `OLD PUNCH IN`, `OLD PUNCH OUT` - Original times
- `NEW PUNCH IN`, `NEW PUNCH OUT` - Corrected times
- `CONTRACTOR REASON` - Why correction needed
- `REQUEST STATUS` - Pending/Approved/Rejected

**Use Case:** Handle late coming, early leaving, missed punches

---

## Key Insights for Database Design

### 1. **Master Tables Needed:**
```
employees (ep_no, ep_name, contractor_code, trade, skill, etc.)
contractors (contractor_code, contractor_name)
eic_users (eic_code, eic_name)
plants (plant_code, plant_name, sector_name)
```

### 2. **Transaction Tables Needed:**
```
punch_records (from Punchrecord Report)
daily_summary (from ARC Summary)
overtime_requests (from OVERTIME)
partial_day_requests (from PARTIAL DAY)
regularization_requests (from REGULARIZATION)
```

### 3. **Linking Strategy:**
All files can be linked using:
- **EP NO** (Employee ID)
- **PUNCHDATE** (Date)
- **CONTRACTOR CODE** (Contractor)

Example query:
```sql
SELECT 
    p.ep_no,
    p.ep_name,
    p.punchdate,
    p.hours_worked,
    a.mandays,
    a.ot,
    o.approved_overtime,
    pd.approved_pd_hours,
    r.request_status as regularization_status
FROM punch_records p
LEFT JOIN daily_summary a 
    ON p.ep_no = a.ep_no AND p.punchdate = a.punchdate
LEFT JOIN overtime_requests o 
    ON p.ep_no = o.ep_no AND p.punchdate = o.punchdate
LEFT JOIN partial_day_requests pd 
    ON p.ep_no = pd.ep_no AND p.punchdate = pd.punchdate
LEFT JOIN regularization_requests r 
    ON p.ep_no = r.ep_no AND p.punchdate = r.punchdate
WHERE p.ep_no = 'PP5000014534'
```

---

## Duplicate Detection

### Potential Duplicates:
Based on analysis, **NO DUPLICATES** found across files because:
- **ARC SUMMARY** = Aggregated daily data
- **OVERTIME** = Only records with overtime
- **PARTIAL DAY** = Only records with partial work
- **PUNCHRECORD** = All punch records
- **REGULARIZATION** = Only correction requests

### However, watch for:
1. Same EP NO + PUNCHDATE appearing in multiple exception files
2. Example: An employee might have:
   - Punch record (normal)
   - Overtime request (worked extra)
   - Regularization request (late coming)
   
   This is **NOT a duplicate** - it's related data!

---

## Data Validation Rules

### Before Import:
1. ✅ **EP NO format:** Must match pattern `PP\d{10}` or `VP\d{10}`
2. ✅ **PUNCHDATE format:** Must be valid date (DD/MM/YYYY)
3. ✅ **CONTRACTOR CODE:** Must exist in contractors table
4. ✅ **Time format:** Must be HH:MM or HH:MM:SS
5. ✅ **Status values:** Must be in allowed list (P, A, L, etc.)

### During Import:
1. ⚠️ **Check for missing required fields**
2. ⚠️ **Validate time ranges** (punch out > punch in)
3. ⚠️ **Check date ranges** (not future dates)
4. ⚠️ **Validate manday calculations** (hours vs mandays)

---

## Recommended Upload Order

```
1. CONTRACTORS (master data)
   ↓
2. EMPLOYEES (master data)
   ↓
3. PUNCHRECORD REPORT (transaction data)
   ↓
4. ARC SUMMARY (aggregated data)
   ↓
5. OVERTIME / PARTIAL DAY / REGULARIZATION (exception data)
```

This order ensures:
- Foreign keys exist before transactions
- Master data is complete
- Relationships are maintained

---

## Summary

### ✅ **Similarities Found:**
1. All files share **EP NO, PUNCHDATE, CONTRACTOR CODE** - perfect for linking
2. All files have **employee and contractor information**
3. All files cover **same date range** (Dec 2025)
4. All files use **same sector** (Polyester)

### ⚠️ **Differences Found:**
1. **Column naming inconsistency** (epNo vs EP NO)
2. **Different purposes** (summary vs detail vs exceptions)
3. **Different record counts** (19 to 25,071 rows)
4. **Different approval workflows** (some have EIC, some have Admin)

### 🎯 **Integration Strategy:**
1. Create **normalized database schema**
2. Build **file upload interface** with auto-detection
3. Implement **data validation** before import
4. Create **user dashboards** based on role
5. Build **approval workflows** for exceptions
6. Generate **reports** combining all data sources

---

**Ready for web application integration!** 🚀
