# Design Document

## Overview

This design document outlines the implementation of an enhanced overstay filtering system that allows users to filter attendance records by specific hour ranges (e.g., "1-2 Hours", "2-3 Hours") rather than just "greater than" thresholds. The enhancement will modify both the backend filtering logic in `core/views.py` and the frontend dropdown options in `core/templates/attendance_list.html`.

## Architecture

The system follows Django's MVT (Model-View-Template) architecture:

1. **Template Layer** (`attendance_list.html`): Renders the filter dropdown with range options
2. **View Layer** (`views.py`): Processes filter parameters and applies filtering logic
3. **Model Layer** (`AttendanceRecord`): Provides the data source for filtering

The filtering logic will be enhanced to support range-based queries while maintaining backward compatibility with existing "has_overstay" and "no_overstay" options.

## Components and Interfaces

### 1. Filter Dropdown Component (Template)

**Location**: `core/templates/attendance_list.html`

**Current Options**:
- `""` - All
- `"has_overstay"` - Has Overstay
- `"no_overstay"` - No Overstay
- `"gt_1"` through `"gt_5"` - Greater than X hours

**New Options**:
- `""` - All
- `"has_overstay"` - Has Overstay
- `"no_overstay"` - No Overstay
- `"range_1_2"` - 1-2 Hours
- `"range_2_3"` - 2-3 Hours
- `"range_3_4"` - 3-4 Hours
- `"range_4_5"` - 4-5 Hours
- `"gte_5"` - 5+ Hours

### 2. Filter Processing Logic (View)

**Location**: `core/views.py` - `attendance_list_view()` and `attendance_export_view()`

**Input**: `overstay_filter` query parameter from GET request

**Output**: Filtered queryset of `AttendanceRecord` objects

**Processing Steps**:
1. Parse the filter value to determine filter type (has/no/range/gte)
2. For range filters, extract min and max hour boundaries
3. Iterate through records with overstay values
4. Parse overstay time strings (format: "HH:MM" or "H:MM")
5. Calculate total hours (hours + minutes/60)
6. Apply range comparison (min <= total_hours < max)
7. Return filtered record IDs
8. Fetch and paginate results

## Data Models

### AttendanceRecord Model

**Relevant Fields**:
- `overstay` (CharField): Stores overstay duration as string (e.g., "02:30", "1:15", "00:00", "-")

**Overstay Format**:
- Valid formats: "HH:MM", "H:MM", "HH:MM:SS"
- Empty/null values: "", "00:00", "-", None
- Examples: "01:30" (1.5 hours), "02:45" (2.75 hours), "05:00" (5 hours)

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Acceptance Criteria Testing Prework

1.1 WHEN a user selects an overstay range filter THEN the Attendance System SHALL display only records where the overstay duration falls within the specified minimum and maximum hour boundaries
Thoughts: This is a universal property that should hold for any range filter selection. We can generate random overstay values and verify that filtered results all fall within the specified range boundaries.
Testable: yes - property

1.2 WHEN the filter dropdown is rendered THEN the Attendance System SHALL display range options in the format "X-Y Hours" where X is the minimum and Y is the maximum hours
Thoughts: This is about UI rendering. We can verify that the HTML contains the expected option elements with correct labels.
Testable: yes - example

1.3 WHEN a user selects "1-2 Hours" THEN the Attendance System SHALL return records with overstay duration greater than or equal to 1 hour AND less than 2 hours
Thoughts: This is a specific instance of the range filtering property. It's covered by property 1.1.
Testable: yes - property (covered by 1.1)

1.4 WHEN a user selects "2-3 Hours" THEN the Attendance System SHALL return records with overstay duration greater than or equal to 2 hours AND less than 3 hours
Thoughts: This is a specific instance of the range filtering property. It's covered by property 1.1.
Testable: yes - property (covered by 1.1)

1.5 WHEN a user selects "3-4 Hours" THEN the Attendance System SHALL return records with overstay duration greater than or equal to 3 hours AND less than 4 hours
Thoughts: This is a specific instance of the range filtering property. It's covered by property 1.1.
Testable: yes - property (covered by 1.1)

2.1 WHEN the filter dropdown is rendered THEN the Attendance System SHALL include an option labeled "5+ Hours" for overstays of 5 hours or greater
Thoughts: This is about UI rendering. We can verify the HTML contains this specific option.
Testable: yes - example

2.2 WHEN a user selects "5+ Hours" THEN the Attendance System SHALL return records with overstay duration greater than or equal to 5 hours with no upper limit
Thoughts: This is a property about filtering with a lower bound but no upper bound. We can generate random overstay values >= 5 hours and verify they're all included.
Testable: yes - property

2.3 WHEN displaying the "5+ Hours" option THEN the Attendance System SHALL position it as the last range option in the dropdown
Thoughts: This is about UI ordering. We can verify the option appears in the correct position in the HTML.
Testable: yes - example

3.1 WHEN the filter dropdown is rendered THEN the Attendance System SHALL maintain the "All" option as the first choice
Thoughts: This is about UI ordering. We can verify the option appears first in the HTML.
Testable: yes - example

3.2 WHEN the filter dropdown is rendered THEN the Attendance System SHALL maintain the "Has Overstay" option to show all records with any overstay duration
Thoughts: This is about UI rendering and backward compatibility. We can verify the option exists.
Testable: yes - example

3.3 WHEN the filter dropdown is rendered THEN the Attendance System SHALL maintain the "No Overstay" option to show all records with no overstay
Thoughts: This is about UI rendering and backward compatibility. We can verify the option exists.
Testable: yes - example

3.4 WHEN the filter dropdown is rendered THEN the Attendance System SHALL display options in this order: "All", "Has Overstay", "No Overstay", followed by hour range options
Thoughts: This is about UI ordering. We can verify the complete order of options in the HTML.
Testable: yes - example

4.1 WHEN parsing overstay time strings THEN the Attendance System SHALL correctly handle various time formats including "HH:MM:SS" and "H:MM:SS"
Thoughts: This is about parsing robustness across different input formats. We can generate random time strings in various formats and verify they parse correctly.
Testable: yes - property

4.2 WHEN an overstay value is exactly at a range boundary THEN the Attendance System SHALL include it in the lower range (e.g., exactly 2 hours belongs to "1-2 Hours" range)
Thoughts: This is about boundary behavior. We can test specific boundary values to ensure they're assigned to the correct range.
Testable: yes - example

4.3 WHEN filtering with hour ranges THEN the Attendance System SHALL maintain performance by using efficient database queries or in-memory filtering as appropriate
Thoughts: This is a performance requirement, not a functional correctness property.
Testable: no

4.4 WHEN no records match the selected range THEN the Attendance System SHALL display an appropriate empty state message
Thoughts: This is about UI behavior when results are empty. We can verify the empty state is displayed correctly.
Testable: yes - example

### Property Reflection

After reviewing all testable properties:

**Redundancies Identified**:
- Properties 1.3, 1.4, and 1.5 are all specific instances of property 1.1 (range filtering). They can be consolidated into a single comprehensive property that tests range filtering for all ranges.
- Properties 1.2, 2.1, 2.3, 3.1, 3.2, 3.3, and 3.4 are all about UI rendering and can be consolidated into a single example test that verifies the complete dropdown structure.

**Consolidated Properties**:
1. **Range filtering correctness** (consolidates 1.1, 1.3, 1.4, 1.5)
2. **Open-ended range filtering** (2.2)
3. **Time format parsing** (4.1)
4. **Dropdown structure** (consolidates 1.2, 2.1, 2.3, 3.1, 3.2, 3.3, 3.4) - example test
5. **Boundary behavior** (4.2) - example test
6. **Empty state display** (4.4) - example test

### Correctness Properties

**Property 1: Range filtering correctness**

*For any* hour range filter (min, max) and any set of attendance records, all returned records should have overstay durations where min <= total_hours < max

**Validates: Requirements 1.1, 1.3, 1.4, 1.5**

**Property 2: Open-ended range filtering**

*For any* minimum hour threshold and any set of attendance records, when filtering with a "greater than or equal" filter (e.g., "5+ Hours"), all returned records should have overstay durations >= the threshold with no upper limit

**Validates: Requirements 2.2**

**Property 3: Time format parsing robustness**

*For any* valid time string in formats "HH:MM", "H:MM", or "HH:MM:SS", the parsing function should correctly extract hours and minutes and calculate total hours as hours + (minutes / 60.0)

**Validates: Requirements 4.1**

## Error Handling

### Invalid Filter Values

**Scenario**: User provides malformed filter parameter (e.g., `overstay_filter=invalid`)

**Handling**: 
- Catch `ValueError` and `IndexError` exceptions during filter parsing
- Log warning message
- Return unfiltered queryset (same as "All" option)
- No error message displayed to user

### Invalid Overstay Format

**Scenario**: Database contains overstay value in unexpected format

**Handling**:
- Wrap parsing logic in try-except block
- Catch `ValueError` and `AttributeError`
- Skip the record (don't include in filtered results)
- Continue processing remaining records
- Log warning for debugging

### Empty Result Set

**Scenario**: No records match the selected range

**Handling**:
- Return empty queryset
- Django pagination handles empty results gracefully
- Template displays "Showing 0 records" message
- No special error handling required

### Large Result Sets

**Scenario**: Range filter matches thousands of records

**Handling**:
- Use iterator with chunk_size=500 to avoid loading all records into memory
- Batch ID fetching in chunks of 999 to avoid SQLite's variable limit
- Apply pagination (50 records per page)
- Maintain existing performance optimization strategy

## Testing Strategy

### Unit Testing

Unit tests will verify specific examples and edge cases:

1. **Filter parsing tests**:
   - Test parsing of each range filter value (range_1_2, range_2_3, etc.)
   - Test parsing of gte_5 filter
   - Test handling of invalid filter values

2. **Overstay parsing tests**:
   - Test parsing "HH:MM" format (e.g., "02:30")
   - Test parsing "H:MM" format (e.g., "1:15")
   - Test parsing "HH:MM:SS" format (e.g., "02:30:00")
   - Test handling of invalid formats

3. **Boundary tests**:
   - Test overstay exactly at 1.0 hours (should be in range_1_2)
   - Test overstay exactly at 2.0 hours (should be in range_2_3)
   - Test overstay at 1.99 hours (should be in range_1_2)
   - Test overstay at 5.0 hours (should be in gte_5)

4. **Empty state tests**:
   - Test filtering when no records match range
   - Verify empty queryset is returned
   - Verify pagination handles empty results

5. **Template rendering tests**:
   - Verify dropdown contains all expected options
   - Verify options are in correct order
   - Verify option labels match specification

### Property-Based Testing

**Framework**: Hypothesis (Python property-based testing library)

**Configuration**: Minimum 100 iterations per property test

Property-based tests will verify universal properties across randomly generated inputs:

1. **Property Test: Range filtering correctness**
   - Generate random attendance records with various overstay values
   - Generate random range filter (min, max)
   - Apply filter
   - Verify all returned records have min <= overstay_hours < max
   - **Feature: overstay-range-filter, Property 1: Range filtering correctness**

2. **Property Test: Open-ended range filtering**
   - Generate random attendance records with various overstay values
   - Apply "5+ Hours" filter
   - Verify all returned records have overstay_hours >= 5.0
   - **Feature: overstay-range-filter, Property 2: Open-ended range filtering**

3. **Property Test: Time format parsing robustness**
   - Generate random time strings in formats "HH:MM", "H:MM", "HH:MM:SS"
   - Parse each time string
   - Verify calculated total_hours matches expected value
   - Verify no exceptions are raised for valid formats
   - **Feature: overstay-range-filter, Property 3: Time format parsing robustness**

### Integration Testing

Integration tests will verify the complete flow:

1. **End-to-end filter test**:
   - Create test attendance records with known overstay values
   - Make GET request with range filter parameter
   - Verify response contains only matching records
   - Verify pagination works correctly

2. **Export functionality test**:
   - Apply range filter
   - Export to XLSX
   - Verify exported file contains only filtered records

3. **Multiple filter combination test**:
   - Apply overstay range filter + date filter + EP NO filter
   - Verify all filters work together correctly

## Implementation Notes

### Filter Value Format

The new filter values will follow the pattern:
- `range_{min}_{max}` for bounded ranges (e.g., `range_1_2`, `range_2_3`)
- `gte_{min}` for open-ended ranges (e.g., `gte_5`)

This format is:
- Easy to parse with string operations
- Self-documenting
- Consistent with existing patterns
- URL-safe

### Backward Compatibility

The implementation will maintain full backward compatibility:
- Existing `has_overstay` and `no_overstay` filters remain unchanged
- Existing `gt_X` filters will be deprecated but continue to work
- No database schema changes required
- No changes to AttendanceRecord model

### Performance Considerations

The current implementation uses in-memory filtering for overstay ranges because:
1. Overstay is stored as a string, not a numeric field
2. Parsing is required to convert "HH:MM" to hours
3. Database-level filtering would require complex SQL string parsing

This approach is acceptable because:
- Pagination limits results to 50 per page
- Iterator with chunk_size=500 prevents memory issues
- Batch fetching avoids SQLite's 999 variable limit
- Performance is adequate for typical dataset sizes

### Code Locations

**Files to modify**:
1. `core/templates/attendance_list.html` - Update dropdown options (2 locations: mobile and desktop)
2. `core/views.py` - Update `attendance_list_view()` function
3. `core/views.py` - Update `attendance_export_view()` function
4. `core/views.py` - Update `export_csv_view()` function (if it exists)

**Functions to modify**:
- `attendance_list_view()` - Main list view with filtering
- `attendance_export_view()` - XLSX export with filtering
- `export_csv_view()` - CSV export with filtering

### Active Filter Display

The template displays active filters as badges. The display logic needs to be updated to show range labels:
- `range_1_2` → "Overstay: 1-2 Hours"
- `range_2_3` → "Overstay: 2-3 Hours"
- `range_3_4` → "Overstay: 3-4 Hours"
- `range_4_5` → "Overstay: 4-5 Hours"
- `gte_5` → "Overstay: 5+ Hours"
