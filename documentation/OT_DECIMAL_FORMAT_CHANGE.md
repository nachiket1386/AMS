# OT Field Changed to Decimal Format

## Changes Made

The "OT" (Overtime) field has been changed from TimeField to DecimalField to store overtime as decimal hours (e.g., "3" instead of "3:00:00").

### Reason for Change:
- User requested OT to be stored as a simple decimal number (e.g., "3" for 3 hours)
- Previously, OT was stored as time format which displayed as "3 a.m." or "03:00:00"
- Now OT is stored as decimal (e.g., "3.00", "2.50") for easier data entry and display

### Files Modified:

1. **core/models.py**
   - Changed `ot` field from `TimeField` to `DecimalField(max_digits=5, decimal_places=2)`

2. **core/manday_processor.py**
   - Updated `process_row` method to validate OT as decimal using `validate_decimal` instead of `validate_time_to_decimal`
   - Removed time conversion for OT field
   - Updated `create_or_update_record` to not convert OT to time object

3. **core/tests/test_manday_models.py**
   - Updated all test cases to use `Decimal` for OT instead of `time` objects
   - Updated property test to generate decimal values for OT (0.00 to 999.99)

4. **sample_mandays.csv**
   - Updated sample data to show decimal format for OT (0, 2.5, 3)

### Database Migration:

Created migration `0007_change_ot_to_decimal.py` which:
- Changes the `ot` field from TimeField to DecimalField
- Migration applied successfully

### Field Comparison:

**Before:**
- `ot = models.TimeField(verbose_name='Overtime')`
- Stored as: 03:00:00
- Displayed as: 3 a.m. or 03:00:00
- CSV format: "3:00" or "03:00"

**After:**
- `ot = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Overtime')`
- Stored as: 3.00
- Displayed as: 3.00 or 3
- CSV format: "3" or "3.00" or "3.5"

### CSV Upload Format:

The updated CSV format accepts decimal numbers for OT:

```csv
epNo,punchDate,mandays,regularMandayHr,ot,trade,contract,plant,plantDesc
EMP001,2024-01-15,1.00,8.00,0,Electrician,CT001,PLT01,Main Plant
EMP002,2024-01-15,1.50,8.50,2.5,Plumber,CT002,PLT01,Main Plant
EMP003,2024-01-16,1.00,8.00,3,Welder,CT001,PLT02,Secondary Plant
```

### Examples:
- `0` → stored as `0.00`
- `3` → stored as `3.00`
- `2.5` → stored as `2.50`
- `8.75` → stored as `8.75`

### Note:
- `regularMandayHr` still accepts both HH:MM format and decimal format (converted to time internally)
- `ot` now only accepts decimal format (no time conversion)

### Testing:

All 21 tests pass successfully after the change.

## Impact:

- Existing data: OT values have been converted from time to decimal format
- CSV uploads: OT field now expects decimal numbers (e.g., "3", "2.5")
- Display: OT will show as decimal numbers (e.g., "3.00", "2.50")
- Excel exports: OT will export as decimal numbers

The feature works correctly with OT as a decimal field.
