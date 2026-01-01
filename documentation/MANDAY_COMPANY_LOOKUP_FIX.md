# Manday Company Lookup Fix

## Problem
When uploading manday summary data, employee records were being assigned to the wrong company. For example, employee "101075428" was showing as belonging to "Company> 99 TACTICS" when they shouldn't be.

## Root Cause
The manday processor (`core/manday_processor.py`) was assigning ALL uploaded records to the admin user's company, regardless of which company the employee actually belongs to. The logic was:

```python
# OLD LOGIC - INCORRECT
if user.role == 'admin':
    company = user.company  # Always uses admin's company
```

This meant that if an admin from "99 TACTICS" uploaded manday data, every employee in that CSV would be assigned to "99 TACTICS", even if they belonged to different companies.

## Solution
The manday processor now looks up the employee's company from their existing **Attendance Records** before assigning the company. This ensures that manday records use the same company as the employee's attendance data.

### New Logic Flow:
1. **Look up employee in AttendanceRecord table** by `ep_no`
2. **If found**: Use the company from their attendance record
3. **If not found**: 
   - For admin users: Use admin's company (with warning log)
   - For root users: Use default company (with warning log)

### Code Changes

```python
# NEW LOGIC - CORRECT
# Get company from existing attendance records for this employee
ep_no_str = str(row['epNo']).strip()

# Try to find the employee's company from their attendance records
from .models import AttendanceRecord
existing_attendance = AttendanceRecord.objects.filter(ep_no=ep_no_str).first()

if existing_attendance:
    # Use the company from the employee's attendance record
    company = existing_attendance.company
else:
    # No attendance record found - use admin's company or fail
    if user.role == 'admin':
        if not user.company:
            return (False, f"Row {row_number}: Admin user must have a company assigned", None)
        company = user.company
        logger.warning(f"Employee {ep_no_str} not found in attendance records. Using admin's company: {company.name}")
    else:
        # Root users can create/use any company
        company = user.company if user.company else Company.objects.first()
        if not company:
            company = Company.objects.create(name="Default Company")
        logger.warning(f"Employee {ep_no_str} not found in attendance records. Using default company: {company.name}")
```

## Benefits
1. **Correct company assignment**: Employees are assigned to their actual company based on attendance data
2. **Data consistency**: Manday records match attendance records for company assignment
3. **Warning logs**: System logs when an employee is not found in attendance records
4. **Backward compatibility**: Still works for new employees (uses admin's company with warning)

## Files Modified
1. `core/manday_processor.py` - Updated `process_row()` method to lookup company from attendance records

## Testing
After applying this fix:
- ✅ Upload manday data for employees with existing attendance records
- ✅ Verify each employee's manday record uses the correct company from their attendance data
- ✅ Check logs for warnings about employees not found in attendance records
- ✅ Verify that employee "101075428" now shows the correct company

## Important Notes
- **Attendance data must be uploaded first**: Employees must have attendance records before uploading manday data for accurate company assignment
- **New employees**: If an employee has no attendance records, their manday data will use the admin's company (with a warning logged)
- **Data integrity**: This ensures manday and attendance data are consistent for company assignments

## Recommendation
For best results, always upload attendance data before uploading manday summary data for the same employees. This ensures the system can correctly determine which company each employee belongs to.
