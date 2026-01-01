# Time Format Fix for Manday Upload

## Problem
The `regularMandayHr` and `ot` fields were expecting HH:MM format (e.g., "08:30") in the CSV upload, but the processor was trying to validate them as decimal numbers, causing validation errors like:
```
Row 2: Invalid or negative value in 'regularMandayHr' field
```

## Root Cause
The database model uses `TimeField` for `regular_manday_hr` and `ot` fields, but the processor was only validating them as decimal numbers without handling the HH:MM time format.

## Solution
Added comprehensive time format handling to the `MandayProcessor` class:

### 1. New Method: `validate_time_to_decimal`
- Accepts both HH:MM format (e.g., "08:30") and decimal format (e.g., "8.5")
- Converts HH:MM to decimal hours for internal processing
- Validates that hours and minutes are in valid ranges

### 2. New Method: `decimal_hours_to_time`
- Converts decimal hours back to Python `time` objects
- Handles edge cases like rounding and hour limits (0-23)
- Required because Django's `TimeField` expects `time` objects

### 3. Updated `process_row` Method
- Uses `validate_time_to_decimal` for both `regularMandayHr` and `ot` fields
- Converts decimal hours to `time` objects before storing in database
- Provides clear error messages for invalid time formats

### 4. Updated `create_or_update_record` Method
- Automatically converts `Decimal` values to `time` objects if needed
- Ensures backward compatibility with existing code

## Supported Formats
The processor now accepts both formats for time fields:

### HH:MM Format
```csv
epNo,punchDate,mandays,regularMandayHr,ot
EMP001,2024-01-15,1.00,08:30,02:15
EMP002,2024-01-15,1.00,09:00,01:30
```

### Decimal Format
```csv
epNo,punchDate,mandays,regularMandayHr,ot
EMP001,2024-01-15,1.00,8.5,2.25
EMP002,2024-01-15,1.00,9.0,1.5
```

## Conversion Examples
- `08:30` → 8.5 hours → `time(8, 30)`
- `09:00` → 9.0 hours → `time(9, 0)`
- `04:15` → 4.25 hours → `time(4, 15)`
- `8.5` → 8.5 hours → `time(8, 30)`

## Testing
All tests pass successfully:
- 21 tests in `test_manday_models` and `test_manday_processor`
- Property-based tests verify time format handling across many inputs
- Unit tests verify specific time conversions

## Files Modified
1. `core/manday_processor.py` - Added time format handling methods
2. `core/tests/test_manday_models.py` - Updated tests to use `time` objects
3. `test_time_parsing.py` - Created test script to verify time parsing

## Usage
Users can now upload CSV files with time values in either format:
- HH:MM format: `08:30`, `09:00`, `04:15`
- Decimal format: `8.5`, `9.0`, `4.25`

Both formats will be correctly processed and stored in the database.
