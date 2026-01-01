# ARC Summary Upload Implementation

## Overview
Added support for uploading and viewing ARC Summary files with specific columns for mandays, trade, contract, and overtime tracking.

## Changes Made

### 1. Database Model Updates (`core/models.py`)

Added new fields to `AttendanceRecord` model:

```python
# ARC Summary specific fields
cont_code = CharField(max_length=50)        # Contractor Code
trade = CharField(max_length=100)           # Trade
contract = CharField(max_length=100)        # Contract
mandays = DecimalField(max_digits=5, decimal_places=2)  # Mandays
regular_manday_hr = CharField(max_length=20)  # Regular Manday Hours
ot = CharField(max_length=20)               # OT
```

Also changed `overtime_to_mandays` from TimeField to CharField for flexibility.

### 2. Migration (`core/migrations/0013_add_arc_summary_fields.py`)

Created migration to:
- Add 6 new ARC Summary fields
- Convert `overtime_to_mandays` from TimeField to CharField
- Make `shift`, `overstay`, and `status` fields optional with defaults

**Applied successfully** ✅

### 3. Data Importer Updates (`core/services/data_importer_service.py`)

Updated `import_attendance_records()` to handle ARC Summary columns:

**Column Mappings Added:**
- `cont_code` / `contcode` → Contractor Code
- `trade` → Trade
- `contract` → Contract  
- `mandays` → Mandays (decimal)
- `regular_manday_hr` / `regularmandayhr` → Regular Manday Hours
- `ot` → OT

**Features:**
- Automatically detects and imports ARC Summary columns
- Handles both Punchrecord and ARC Summary file formats
- Stores contractor code in `cont_code` field
- Converts mandays to decimal format
- Stores regular hours and OT as strings

### 4. ARC Summary Report Template (`core/templates/reports/arc_summary.html`)

Updated to display ARC Summary specific columns:

**Columns Displayed:**
1. EP NO
2. DATE
3. CONT CODE (Contractor Code)
4. TRADE
5. CONTRACT
6. MANDAYS
7. REGULAR HR (Regular Manday Hours)
8. OT (Overtime)

**Features:**
- Clean, focused layout for ARC Summary data
- Falls back to company name if cont_code is empty
- Shows "-" for empty fields
- Responsive design with horizontal scroll

## Upload Requirements

### ARC Summary File Format

**Required Columns:**
- `epNo` or `ep_no` - Employee Number
- `punchDate` or `date` - Date
- `contCode` - Contractor Code
- `trade` - Trade
- `contract` - Contract
- `mandays` - Mandays (decimal, e.g., 1.0, 0.5)
- `regularMandayHr` - Regular Manday Hours
- `ot` - Overtime

**Optional Columns:**
- `ep_name` - Employee Name
- `shift` - Shift
- `status` - Status (P, A, PH, etc.)

### Example ARC Summary Data

```csv
epNo,punchDate,contCode,trade,contract,mandays,regularMandayHr,ot
PP5000039067,2025-12-01,176667,QAQC Tester,Main Contract,1.0,08:00,02:00
PP5000039081,2025-12-01,176667,QAQC Tester,Main Contract,1.0,08:00,00:00
PP5000039084,2025-12-01,176667,QAQC Tester,Main Contract,0.5,04:00,00:00
```

## How to Use

### 1. Upload ARC Summary File

1. Go to `/excel/upload/`
2. Select "ARC Summary" file type
3. Upload your Excel file with ARC Summary columns
4. System auto-detects columns and imports data
5. Real-time progress shows row-by-row import

### 2. View ARC Summary Report

1. Go to `/attendance/` or any page with report tabs
2. Click "📊 ARC Summary" tab
3. View data with columns: EP NO, DATE, CONT CODE, TRADE, CONTRACT, MANDAYS, REGULAR HR, OT
4. Use filters to search by EP NO, date range
5. Export to Excel if needed

## Benefits

✅ **Unified Data Model** - Both Punchrecord and ARC Summary data in one table
✅ **Flexible Import** - Automatically detects file type and columns
✅ **Dedicated Report** - Clean view of ARC Summary specific data
✅ **No Data Loss** - All columns preserved in database
✅ **Easy Filtering** - Filter by EP, date, company
✅ **Role-Based Access** - Root sees all, Admin sees their company, User1 sees assigned EPs

## Data Flow

```
ARC Summary Excel File
    ↓
Upload (auto-detect columns)
    ↓
Validate (check required fields)
    ↓
Import to AttendanceRecord
    ↓
View in ARC Summary Report
```

## Database Schema

The `AttendanceRecord` model now supports both file types:

**Punchrecord Fields:**
- ep_no, ep_name, company, date, shift, status
- in_time, out_time, in_time_2, out_time_2, in_time_3, out_time_3
- hours, overstay, overtime

**ARC Summary Fields:**
- cont_code, trade, contract
- mandays, regular_manday_hr, ot

**Shared Fields:**
- ep_no, date (unique together)
- company (foreign key)
- created_at, updated_at

## Testing

To test ARC Summary upload:

1. **Prepare Test File:**
   - Create Excel file with columns: epNo, punchDate, contCode, trade, contract, mandays, regularMandayHr, ot
   - Add sample data rows

2. **Upload:**
   - Navigate to `/excel/upload/`
   - Select "ARC Summary"
   - Upload file
   - Watch real-time progress

3. **Verify:**
   - Check import results (imported count, duplicates)
   - Go to ARC Summary report tab
   - Verify all columns display correctly
   - Test filters (EP NO, date range)

4. **Check Data:**
   - Verify mandays stored as decimal
   - Verify cont_code, trade, contract populated
   - Verify regular_manday_hr and ot stored correctly

## Notes

- ARC Summary and Punchrecord data can coexist in the same table
- Records are identified by (ep_no, date) combination
- Uploading same EP + date updates existing record
- All ARC Summary fields are optional (blank allowed)
- Mandays field accepts decimal values (e.g., 0.5, 1.0, 1.5)
- Regular hours and OT stored as strings for flexibility

## Future Enhancements

Possible improvements:
- Separate ARC Summary upload validation rules
- Mandays calculation from hours
- OT approval workflow
- Trade-based reporting
- Contract-based filtering
- Mandays summary by contractor
