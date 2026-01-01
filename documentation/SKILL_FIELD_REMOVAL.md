# Skill Field Removal from Mandays & Overtime Summary

## Changes Made

The "Skill" field has been completely removed from the Mandays & Overtime Summary feature.

### Files Modified:

1. **core/models.py**
   - Removed `skill` field from `MandaySummaryRecord` model

2. **core/manday_processor.py**
   - Removed `'skill'` from `OPTIONAL_FIELDS` list
   - Removed `'SKILL': 'skill'` from `COLUMN_ALIASES` dictionary
   - Removed skill field from data dictionary in `process_row` method

3. **core/templates/mandays_list.html**
   - Removed "Skill" column header from table
   - Removed skill data cell from table rows
   - Updated colspan from 10 to 9 for empty state message

4. **core/views.py** (mandays_export_view)
   - Removed 'SKILL' from export headers
   - Removed skill column from Excel export data
   - Adjusted column numbers for remaining fields

5. **core/admin.py**
   - Removed 'skill' from `list_filter`
   - Removed 'skill' from `search_fields`
   - Removed 'skill' from fieldsets

6. **core/tests/test_manday_processor.py**
   - Removed skill assertions from tests
   - Removed skill from test data dictionaries

7. **core/tests/test_manday_models.py**
   - Removed skill assertions from tests

8. **sample_mandays.csv**
   - Removed skill column from sample CSV file

### Database Migration:

Created migration `0006_remove_skill_field.py` which:
- Removes the `skill` field from the `MandaySummaryRecord` table
- Migration applied successfully

### Current Optional Fields:

The following optional fields remain in the Mandays & Overtime Summary:
- Trade
- Contract
- Plant
- Plant Description

### CSV Upload Format:

The updated CSV format no longer includes the skill column:

```csv
epNo,punchDate,mandays,regularMandayHr,ot,trade,contract,plant,plantDesc
EMP001,2024-01-15,1.00,8.00,0.00,Electrician,CT001,PLT01,Main Plant
```

### Testing:

All 21 tests pass successfully after the removal of the skill field.

## Impact:

- Existing data: The skill column data has been removed from the database
- CSV uploads: Files with skill column will ignore it (it's no longer in OPTIONAL_FIELDS)
- Excel exports: No longer include skill column
- List view: No longer displays skill column
- Admin interface: No longer shows or filters by skill

The feature continues to work normally with the remaining optional fields.
