# Overstay Filter Enhancement

## Overview
Enhanced the Attendance Data page with granular overstay filtering options, allowing users to filter records by specific hour thresholds.

## Changes Made

### 1. Template Updates (`core/templates/attendance_list.html`)

#### Mobile Filter Section
Added new overstay filter options:
- All
- Has Overstay
- No Overstay
- **> 1 Hour** (NEW)
- **> 2 Hours** (NEW)
- **> 3 Hours** (NEW)
- **> 4 Hours** (NEW)
- **> 5 Hours** (NEW)

#### Desktop Filter Section
Same options added to desktop view for consistency.

#### Active Filters Display
Updated to show the selected hour threshold in the active filters badge:
- "Overstay > 1 Hour"
- "Overstay > 2 Hours"
- etc.

### 2. Backend Logic (`core/views.py`)

#### Overstay Parsing Algorithm
Implemented intelligent overstay time parsing:
```python
# Parse format: "02:30", "1:15", "00:45"
parts = overstay_str.split(':')
overstay_hours = int(parts[0])
overstay_minutes = int(parts[1])
total_hours = overstay_hours + (overstay_minutes / 60.0)
```

#### Filter Implementation
- `has_overstay`: Shows all records with any overstay
- `no_overstay`: Shows records with no overstay
- `gt_1` through `gt_5`: Shows records where overstay > X hours

#### Updated Functions
1. `attendance_list_view()` - Main list view with pagination
2. `attendance_export_view()` - XLSX export
3. `export_csv_view()` - CSV export

All three functions now support hour-based filtering.

### 3. Filter Logic Flow

```
User selects "> 2 Hours"
    ↓
Backend receives: overstay_filter='gt_2'
    ↓
Extract hours: hours = 2
    ↓
Get all records with overstay
    ↓
Parse each overstay time (HH:MM format)
    ↓
Calculate total hours (including minutes as decimal)
    ↓
Filter records where total_hours > 2
    ↓
Return filtered queryset
```

## Usage Examples

### Example 1: Find all records with overstay > 3 hours
1. Navigate to Attendance Data page
2. Select "Overstay" dropdown
3. Choose "> 3 Hours"
4. Click "Filter"

Result: Only records with overstay greater than 3 hours will be displayed.

### Example 2: Export records with overstay > 1 hour
1. Apply "> 1 Hour" filter
2. Click "Download XLSX"
3. Exported file contains only filtered records

## Technical Details

### Overstay Format Support
The filter handles various overstay formats:
- `02:30` → 2.5 hours
- `1:15` → 1.25 hours
- `00:45` → 0.75 hours
- `5:00` → 5.0 hours

### Edge Cases Handled
- Empty overstay values
- "00:00" (no overstay)
- "-" (no data)
- Null values
- Invalid formats (gracefully skipped)

### Performance Considerations
- Initial queryset filters out empty/null overstay values
- Only parses overstay times for records that have values
- Uses ID-based filtering for final queryset
- Efficient for datasets with mixed overstay values

## Testing Recommendations

1. **Basic Filtering**
   - Test each hour threshold (1-5 hours)
   - Verify correct records are displayed

2. **Edge Cases**
   - Records with exactly 1:00, 2:00, etc. (should not appear in > filters)
   - Records with 1:01, 2:01, etc. (should appear)
   - Mixed format overstay values

3. **Export Functionality**
   - XLSX export with each filter option
   - CSV export with each filter option
   - Verify exported data matches filtered view

4. **Pagination**
   - Apply filter and navigate through pages
   - Verify filter persists across pages

5. **Combined Filters**
   - Overstay + Date range
   - Overstay + Status
   - Overstay + EP NO search

## Future Enhancements

Potential improvements:
1. Custom hour input (e.g., "> X hours" where X is user-defined)
2. Range filters (e.g., "1-3 hours", "3-5 hours")
3. Overstay statistics dashboard
4. Overstay trend analysis
5. Configurable hour thresholds per company

## Server Status
✅ Server automatically reloaded with changes
✅ No syntax errors detected
✅ Ready for testing at http://127.0.0.1:8000/attendance/
