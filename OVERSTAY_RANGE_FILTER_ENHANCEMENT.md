# Overstay Range Filter Enhancement

## Summary
Enhanced the overstay filter in the Attendance Data page to include granular hour ranges, making it easier to filter records by specific overstay durations.

## Changes Made

### 1. Template Updates (`core/templates/attendance_list.html`)

**Filter Dropdown Options:**
- Replaced generic "> X Hours" options with specific hour ranges
- New options:
  - `1-2 Hours` (range_1_2)
  - `2-3 Hours` (range_2_3)
  - `3-4 Hours` (range_3_4)
  - `4-5 Hours` (range_4_5)
  - `> 5 Hours` (gt_5) - kept for records exceeding 5 hours

**Active Filter Display:**
- Updated to show range labels (e.g., "Overstay: 1-2 Hours")

### 2. Backend Logic Updates (`core/views.py`)

**Functions Updated:**
1. `attendance_list_view()` - Main list view
2. `attendance_export_view()` - XLSX export
3. `export_csv_view()` - CSV export

**New Range Filter Logic:**
- Parses `range_X_Y` format (e.g., `range_1_2` for 1-2 hours)
- Filters records where overstay is >= min_hours and < max_hours
- Handles time parsing from "HH:MM" format
- Converts to decimal hours for comparison
- Uses chunked queries to avoid SQLite's 999 variable limit

**Example:**
- Filter: `range_2_3`
- Matches: Records with overstay between 2:00 and 2:59 hours
- Excludes: Records with exactly 3:00 hours or more

## Benefits

1. **More Precise Filtering**: Users can now filter by specific hour ranges instead of just "greater than"
2. **Better Data Analysis**: Easier to identify patterns in specific overstay durations
3. **Consistent Experience**: Same filter options available in list view and exports
4. **Performance**: Efficient chunked processing for large datasets

## Usage

1. Navigate to Attendance Data page
2. Select "Overstay" filter dropdown
3. Choose desired range (e.g., "2-3 Hours")
4. Click "Filter" to apply
5. Export functionality preserves the selected filter

## Technical Details

**Filter Value Format:**
- `range_MIN_MAX` where MIN and MAX are integers representing hours
- Example: `range_1_2` = 1 to 2 hours

**Time Parsing:**
- Converts "HH:MM" format to decimal hours
- Example: "02:30" = 2.5 hours
- Comparison: `min_hours <= total_hours < max_hours`

**Database Handling:**
- Processes records in chunks of 500 for memory efficiency
- Splits result IDs into batches of 900 for SQLite compatibility
- Uses Q objects for complex OR queries across chunks
