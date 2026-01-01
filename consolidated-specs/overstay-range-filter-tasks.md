# Implementation Plan

- [ ] 1. Update template dropdown options for range-based filtering
  - Modify `core/templates/attendance_list.html` to replace "greater than" options with range options
  - Update both mobile and desktop dropdown sections
  - Change option values from `gt_X` to `range_X_Y` format
  - Add `gte_5` option for "5+ Hours"
  - Update option labels to show ranges (e.g., "1-2 Hours", "2-3 Hours")
  - _Requirements: 1.2, 2.1, 2.3, 3.1, 3.2, 3.3, 3.4_

- [ ] 2. Update active filter display badges
  - Modify the active filter display section in `attendance_list.html`
  - Add template logic to display range labels for new filter values
  - Map `range_1_2` → "Overstay: 1-2 Hours"
  - Map `range_2_3` → "Overstay: 2-3 Hours"
  - Map `range_3_4` → "Overstay: 3-4 Hours"
  - Map `range_4_5` → "Overstay: 4-5 Hours"
  - Map `gte_5` → "Overstay: 5+ Hours"
  - _Requirements: 1.2_

- [ ] 3. Implement range filter parsing logic in attendance_list_view
  - Modify `core/views.py` - `attendance_list_view()` function
  - Add parsing logic for `range_X_Y` filter format
  - Extract min and max hour boundaries from filter value
  - Add parsing logic for `gte_X` filter format
  - Extract minimum hour threshold for open-ended ranges
  - Maintain backward compatibility with existing `has_overstay` and `no_overstay` filters
  - _Requirements: 1.1, 2.2, 4.1_

- [ ] 4. Implement range-based filtering logic
  - In `attendance_list_view()`, implement range comparison logic
  - For range filters: check if min <= total_hours < max
  - For gte filters: check if total_hours >= min
  - Handle boundary cases correctly (inclusive lower bound, exclusive upper bound)
  - Maintain existing iterator and batch fetching for performance
  - _Requirements: 1.1, 1.3, 1.4, 1.5, 2.2, 4.2_

- [ ] 4.1 Write property test for range filtering correctness
  - **Property 1: Range filtering correctness**
  - **Validates: Requirements 1.1, 1.3, 1.4, 1.5**

- [ ] 4.2 Write property test for open-ended range filtering
  - **Property 2: Open-ended range filtering**
  - **Validates: Requirements 2.2**

- [ ] 4.3 Write property test for time format parsing
  - **Property 3: Time format parsing robustness**
  - **Validates: Requirements 4.1**

- [ ] 5. Update attendance_export_view with range filtering
  - Modify `core/views.py` - `attendance_export_view()` function
  - Apply same range filter parsing logic as attendance_list_view
  - Implement same range-based filtering logic
  - Ensure XLSX export includes only filtered records
  - _Requirements: 1.1, 2.2_

- [ ] 6. Update export_csv_view with range filtering
  - Modify `core/views.py` - `export_csv_view()` function (if it exists)
  - Apply same range filter parsing logic
  - Implement same range-based filtering logic
  - Ensure CSV export includes only filtered records
  - _Requirements: 1.1, 2.2_

- [ ] 7. Write unit tests for filter parsing
  - Test parsing of `range_1_2`, `range_2_3`, `range_3_4`, `range_4_5` formats
  - Test parsing of `gte_5` format
  - Test handling of invalid filter values
  - Test backward compatibility with `has_overstay` and `no_overstay`

- [ ] 8. Write unit tests for overstay time parsing
  - Test parsing "HH:MM" format (e.g., "02:30")
  - Test parsing "H:MM" format (e.g., "1:15")
  - Test parsing "HH:MM:SS" format (e.g., "02:30:00")
  - Test handling of invalid formats
  - Test handling of empty/null values

- [ ] 9. Write unit tests for boundary cases
  - Test overstay exactly at 1.0 hours (should be in range_1_2)
  - Test overstay exactly at 2.0 hours (should be in range_2_3)
  - Test overstay at 1.99 hours (should be in range_1_2)
  - Test overstay at 5.0 hours (should be in gte_5)

- [ ] 10. Write integration tests for end-to-end filtering
  - Create test attendance records with known overstay values
  - Test GET request with range filter parameter
  - Verify response contains only matching records
  - Verify pagination works correctly
  - Test export functionality with range filters
  - Test multiple filter combinations (overstay + date + EP NO)

- [ ] 11. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
