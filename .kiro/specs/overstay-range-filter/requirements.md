# Requirements Document

## Introduction

This feature enhances the overstay filter in the attendance management system to show records within specific hour ranges rather than just "greater than" thresholds. This provides more precise filtering capabilities for supervisors and administrators to identify attendance records with overstay durations within specific time brackets.

## Glossary

- **Overstay**: The duration of time a person remains on premises beyond their scheduled departure time
- **Attendance System**: The web application that tracks and manages attendance records
- **Filter Dropdown**: The HTML select element that allows users to filter attendance records by overstay duration
- **Hour Range**: A specific time bracket defined by a minimum and maximum number of hours (e.g., 1-2 hours, 2-3 hours)

## Requirements

### Requirement 1

**User Story:** As a supervisor, I want to filter attendance records by specific overstay hour ranges, so that I can identify records within precise time brackets rather than just viewing all records above a threshold.

#### Acceptance Criteria

1. WHEN a user selects an overstay range filter THEN the Attendance System SHALL display only records where the overstay duration falls within the specified minimum and maximum hour boundaries
2. WHEN the filter dropdown is rendered THEN the Attendance System SHALL display range options in the format "X-Y Hours" where X is the minimum and Y is the maximum hours
3. WHEN a user selects "1-2 Hours" THEN the Attendance System SHALL return records with overstay duration greater than or equal to 1 hour AND less than 2 hours
4. WHEN a user selects "2-3 Hours" THEN the Attendance System SHALL return records with overstay duration greater than or equal to 2 hours AND less than 3 hours
5. WHEN a user selects "3-4 Hours" THEN the Attendance System SHALL return records with overstay duration greater than or equal to 3 hours AND less than 4 hours

### Requirement 2

**User Story:** As a supervisor, I want to see an option for overstays of 5 hours or more, so that I can identify extreme overstay cases that exceed all defined ranges.

#### Acceptance Criteria

1. WHEN the filter dropdown is rendered THEN the Attendance System SHALL include an option labeled "5+ Hours" for overstays of 5 hours or greater
2. WHEN a user selects "5+ Hours" THEN the Attendance System SHALL return records with overstay duration greater than or equal to 5 hours with no upper limit
3. WHEN displaying the "5+ Hours" option THEN the Attendance System SHALL position it as the last range option in the dropdown

### Requirement 3

**User Story:** As a supervisor, I want the existing "Has Overstay" and "No Overstay" options to remain available, so that I can still perform broad filtering when I don't need specific hour ranges.

#### Acceptance Criteria

1. WHEN the filter dropdown is rendered THEN the Attendance System SHALL maintain the "All" option as the first choice
2. WHEN the filter dropdown is rendered THEN the Attendance System SHALL maintain the "Has Overstay" option to show all records with any overstay duration
3. WHEN the filter dropdown is rendered THEN the Attendance System SHALL maintain the "No Overstay" option to show all records with no overstay
4. WHEN the filter dropdown is rendered THEN the Attendance System SHALL display options in this order: "All", "Has Overstay", "No Overstay", followed by hour range options

### Requirement 4

**User Story:** As a developer, I want the overstay range filtering logic to handle edge cases correctly, so that the system produces accurate results for all valid inputs.

#### Acceptance Criteria

1. WHEN parsing overstay time strings THEN the Attendance System SHALL correctly handle various time formats including "HH:MM:SS" and "H:MM:SS"
2. WHEN an overstay value is exactly at a range boundary THEN the Attendance System SHALL include it in the lower range (e.g., exactly 2 hours belongs to "1-2 Hours" range)
3. WHEN filtering with hour ranges THEN the Attendance System SHALL maintain performance by using efficient database queries or in-memory filtering as appropriate
4. WHEN no records match the selected range THEN the Attendance System SHALL display an appropriate empty state message
