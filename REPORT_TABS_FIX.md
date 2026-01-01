# Report Tabs Fix - Query AttendanceRecord Model

## Issue
After uploading data, the main attendance list showed records correctly, but all report tabs (ARC Summary, Overtime, Partial Day, Regularization) showed "No records found".

## Root Cause
The report views were querying separate models (`DailySummary`, `OvertimeRequest`, `PartialDayRequest`, `RegularizationRequest`) that were not being populated during import. The data was only being imported to the `AttendanceRecord` model.

## Solution
Updated all report views and templates to query the `AttendanceRecord` model instead of separate models.

## Changes Made

### 1. Backend - Report Views (`core/views.py`)

#### ARC Summary Report
**Before:** Queried `DailySummary` model with `employee` foreign key
**After:** Queries `AttendanceRecord` model directly

**Changes:**
- Query: `AttendanceRecord.objects.select_related('company').all()`
- Filters: `ep_no`, `date`, `company`
- Fields displayed: ep_no, ep_name, company, date, shift, status, hours, overstay, overtime

#### Overtime Report
**Before:** Queried `OvertimeRequest` model
**After:** Queries `AttendanceRecord` with overtime filter

**Changes:**
- Query: `AttendanceRecord.objects.exclude(overtime__isnull=True).exclude(overtime='')`
- Shows only records that have overtime values
- Fields displayed: ep_no, ep_name, company, date, shift, hours, overstay, overtime, status

#### Partial Day Report
**Before:** Queried `PartialDayRequest` model
**After:** Queries `AttendanceRecord` with PD status filter

**Changes:**
- Query: `AttendanceRecord.objects.filter(status='PD')`
- Shows only records with Partial Day status
- Fields displayed: ep_no, ep_name, company, date, shift, hours, in_time, out_time, status

#### Regularization Report
**Before:** Queried `RegularizationRequest` model
**After:** Queries all `AttendanceRecord` records

**Changes:**
- Query: `AttendanceRecord.objects.all()`
- Shows all attendance records for regularization tracking
- Fields displayed: ep_no, ep_name, company, date, shift, in_time, out_time, hours, status

### 2. Frontend - Report Templates

#### Updated Field Mappings

**Old Model Fields → New AttendanceRecord Fields:**
- `record.employee.ep_no` → `record.ep_no`
- `record.employee.ep_name` → `record.ep_name`
- `record.employee.contractor.contractor_name` → `record.company.name`
- `record.punchdate` → `record.date`
- `record.mandays` → `record.hours` (hours worked)
- `record.regular_manday_hr` → `record.overtime_to_mandays`
- `record.ot` → `record.overtime`

#### Template Files Updated:
1. `core/templates/reports/arc_summary.html`
2. `core/templates/reports/overtime.html`
3. `core/templates/reports/partial_day.html`
4. `core/templates/reports/regularization.html`

### 3. Access Control Maintained

All reports maintain role-based access control:

**Root Users:**
- See all records across all companies

**Admin Users:**
- See only records from their assigned company
- Filter: `queryset.filter(company=request.user.company)`

**User1 (Supervisors):**
- See only records for employees they have access to
- Uses `AccessControlService` to get accessible EP numbers

## Testing

To verify the fix:

1. **Upload Data:**
   - Go to `/excel/upload/`
   - Upload a punchrecord Excel file
   - Data imports to AttendanceRecord

2. **Check Main Attendance List:**
   - Go to `/attendance/`
   - Should see uploaded records ✅

3. **Check Report Tabs:**
   - Click "📊 ARC Summary" tab
   - Should see all uploaded records ✅
   
   - Click "⏰ Overtime" tab
   - Should see records with overtime values ✅
   
   - Click "📅 Partial Day" tab
   - Should see records with PD status ✅
   
   - Click "✏️ Regularization" tab
   - Should see all records ✅

## Benefits

✅ **Single Source of Truth** - All data in AttendanceRecord model
✅ **Consistent Data** - No sync issues between models
✅ **Simpler Architecture** - Fewer models to maintain
✅ **Better Performance** - Direct queries without joins
✅ **Easier Maintenance** - One model to update

## Data Model

The `AttendanceRecord` model now serves as the unified data store:

```python
class AttendanceRecord(models.Model):
    ep_no = CharField          # Employee number
    ep_name = CharField         # Employee name
    company = ForeignKey        # Company/Contractor
    date = DateField            # Attendance date
    shift = CharField           # Shift code
    status = CharField          # P, A, PH, PD, L, WO
    in_time = TimeField         # Punch in time
    out_time = TimeField        # Punch out time
    hours = CharField           # Hours worked (HH:MM)
    overstay = CharField        # Overstay time (HH:MM)
    overtime = TimeField        # Overtime hours
    overtime_to_mandays = CharField  # OT to mandays conversion
```

## Future Considerations

If you need separate request/approval workflows for overtime, partial day, or regularization:

1. Keep the separate models (`OvertimeRequest`, etc.)
2. Create separate upload flows for those specific file types
3. Use those models for approval workflows
4. Keep `AttendanceRecord` as the master attendance data

For now, all attendance data flows through `AttendanceRecord` which simplifies the system.
