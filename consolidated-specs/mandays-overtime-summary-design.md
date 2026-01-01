# Design Document: Mandays and Overtime Summary

## Overview

This feature adds a new data management capability to the attendance management system for tracking final mandays and overtime records. The system will provide a dedicated upload interface similar to the existing attendance upload, with specialized validation for manday-specific fields. The feature follows the existing architectural patterns established in the system, including role-based access control, CSV/Excel processing, and audit logging.

## Architecture

The feature will integrate into the existing Django-based attendance management system using the established MVC pattern:

- **Models**: New `MandaySummaryRecord` and `MandayUploadLog` models
- **Views**: New view functions for upload, list, and export operations
- **Processor**: New `MandayProcessor` class for file validation and processing
- **Templates**: New HTML templates for upload and list views
- **URLs**: New URL patterns under `/mandays/` namespace

The architecture maintains separation of concerns:
- Data models handle persistence and validation
- Processor classes handle business logic for file processing
- Views orchestrate user interactions
- Services handle cross-cutting concerns (access control, logging)

## Components and Interfaces

### 1. Data Models (`core/models.py`)

#### MandaySummaryRecord
```python
class MandaySummaryRecord(models.Model):
    # Mandatory fields
    ep_no = models.CharField(max_length=50, verbose_name='Employee Number')
    punch_date = models.DateField(verbose_name='Punch Date')
    mandays = models.DecimalField(max_digits=5, decimal_places=2)
    regular_manday_hr = models.DecimalField(max_digits=5, decimal_places=2)
    ot = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Overtime')
    
    # Optional fields
    trade = models.CharField(max_length=100, blank=True, null=True)
    skill = models.CharField(max_length=100, blank=True, null=True)
    contract = models.CharField(max_length=100, blank=True, null=True)
    plant = models.CharField(max_length=100, blank=True, null=True)
    plant_desc = models.CharField(max_length=255, blank=True, null=True)
    
    # Metadata
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['ep_no', 'punch_date']
        ordering = ['-punch_date', 'ep_no']
        indexes = [
            models.Index(fields=['ep_no', 'punch_date']),
            models.Index(fields=['company', 'punch_date']),
            models.Index(fields=['punch_date']),
        ]
```

#### MandayUploadLog
```python
class MandayUploadLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    success_count = models.IntegerField(default=0)
    updated_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    error_messages = models.TextField(blank=True)
```

### 2. Processor Class (`core/manday_processor.py`)

```python
class MandayProcessor:
    REQUIRED_FIELDS = ['epNo', 'punchDate', 'mandays', 'regularMandayHr', 'ot']
    OPTIONAL_FIELDS = ['trade', 'skill', 'contract', 'plant', 'plantDesc']
    
    def validate_csv(self, file) -> dict
    def validate_date(self, date_str) -> date
    def validate_decimal(self, value, field_name) -> Decimal
    def process_row(self, row, row_number, user) -> tuple
    def create_or_update_record(self, data) -> tuple
    def process_csv(self, file, user) -> dict
```

### 3. View Functions (`core/views.py`)

```python
@role_required(['root', 'admin'])
def upload_mandays_view(request):
    """Handle manday file upload and processing"""
    
@login_required
@company_access_required
def mandays_list_view(request):
    """List manday records with filtering and pagination"""
    
@login_required
@company_access_required
def mandays_export_view(request):
    """Export manday records to XLSX"""
    
@role_required(['root', 'admin'])
def download_mandays_template(request):
    """Download empty CSV template"""
```

### 4. URL Patterns (`core/urls.py`)

```python
path('mandays/upload/', views.upload_mandays_view, name='upload_mandays'),
path('mandays/', views.mandays_list_view, name='mandays_list'),
path('mandays/export/', views.mandays_export_view, name='mandays_export'),
path('mandays/template/', views.download_mandays_template, name='download_mandays_template'),
```

### 5. Templates

- `core/templates/upload_mandays.html` - Upload interface
- `core/templates/mandays_list.html` - List/view interface

## Data Models

### MandaySummaryRecord Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ep_no | CharField(50) | Yes | Employee number |
| punch_date | DateField | Yes | Date of work |
| mandays | Decimal(5,2) | Yes | Number of mandays |
| regular_manday_hr | Decimal(5,2) | Yes | Regular manday hours |
| ot | Decimal(5,2) | Yes | Overtime hours |
| trade | CharField(100) | No | Employee trade/category |
| skill | CharField(100) | No | Skill level |
| contract | CharField(100) | No | Contract identifier |
| plant | CharField(100) | No | Plant code |
| plant_desc | CharField(255) | No | Plant description |
| company | ForeignKey | Yes | Associated company |

### Relationships

- MandaySummaryRecord → Company (Many-to-One)
- MandayUploadLog → User (Many-to-One)

### Constraints

- Unique constraint on (ep_no, punch_date) to prevent duplicate entries
- Decimal fields must be >= 0
- Date fields cannot be in the future

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: File format validation
*For any* uploaded file, if the file extension is not CSV, XLS, or XLSX, then the system should reject the file with an appropriate error message
**Validates: Requirements 1.2, 1.4**

### Property 2: Mandatory column presence
*For any* uploaded file, if any of the mandatory columns (epNo, punchDate, mandays, regularMandayHr, ot) are missing from the file headers, then the system should reject the entire file and report which columns are missing
**Validates: Requirements 2.1, 2.2**

### Property 3: Mandatory field validation
*For any* row in an uploaded file, if any mandatory field (epNo, punchDate, mandays, regularMandayHr, ot) contains an empty or null value, then that row should be rejected with a validation error
**Validates: Requirements 2.3, 2.4, 2.5**

### Property 4: Column extraction
*For any* uploaded file containing the specified columns, the system should extract only the defined columns (epNo, punchDate, trade, skill, contract, plant, mandays, regularMandayHr, ot, plantDesc) and ignore any additional columns
**Validates: Requirements 3.1, 3.2**

### Property 5: Optional field handling
*For any* row where optional fields (trade, skill, contract, plant, plantDesc) are missing or empty, the system should store NULL or empty values for those fields without rejecting the row
**Validates: Requirements 3.3**

### Property 6: Numeric data type preservation
*For any* numeric field (mandays, regularMandayHr, ot), the system should preserve the numeric data type and precision when storing values
**Validates: Requirements 3.4**

### Property 7: Upload results reporting
*For any* completed file upload, the system should display the total number of rows processed, number of successful imports, and number of failed records
**Validates: Requirements 4.1, 4.2, 4.3**

### Property 8: Error detail reporting
*For any* validation error that occurs during processing, the system should display the row number and specific error description
**Validates: Requirements 4.4**

### Property 9: Date format validation
*For any* punchDate value, the system should accept standard date formats (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY) and reject invalid or future dates
**Validates: Requirements 5.2**

### Property 10: Numeric field validation
*For any* numeric field (mandays, regularMandayHr, ot), if the value is non-numeric or negative, then the system should reject that row with a data type error
**Validates: Requirements 5.3, 5.4, 5.5, 5.6**

### Property 11: Access control enforcement
*For any* user with USER1 role attempting to access the mandays upload page, the system should deny access and display an authorization error
**Validates: Requirements 7.1**

### Property 12: Admin access grant
*For any* user with USER2 or USER3 role accessing the mandays upload page, the system should grant access to the upload functionality
**Validates: Requirements 7.2**

### Property 13: Company data isolation
*For any* admin user uploading manday data, all created records should be associated with that admin's assigned company, maintaining data isolation
**Validates: Requirements 7.2 (implicit)**

## Error Handling

### File Upload Errors
- Invalid file format → User-friendly error message, redirect to upload page
- File size exceeds limit → Error message with size limit information
- Missing file → Error message prompting file selection

### Validation Errors
- Missing mandatory columns → List all missing columns, reject file
- Invalid data types → Row-level error with field name and expected type
- Future dates → Row-level error indicating date cannot be in future
- Negative numeric values → Row-level error indicating values must be >= 0
- Empty mandatory fields → Row-level error identifying missing field

### Processing Errors
- Database connection errors → Log error, display generic error message
- Duplicate key violations → Update existing record (upsert behavior)
- Permission errors → Access denied message, redirect to dashboard

### Error Logging
- All errors logged to application log with user context
- Upload logs stored in database for audit trail
- Error messages truncated in UI (first 5 errors shown, with count of remaining)

## Testing Strategy

### Unit Testing

Unit tests will verify specific examples and edge cases:

1. **File Validation Tests**
   - Valid CSV file with all required columns
   - Invalid file format (e.g., .txt, .pdf)
   - Empty file
   - File with missing mandatory columns

2. **Data Validation Tests**
   - Valid date formats (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY)
   - Invalid date formats
   - Future dates (should be rejected)
   - Valid numeric values (positive decimals)
   - Invalid numeric values (negative, non-numeric)
   - Empty mandatory fields

3. **Access Control Tests**
   - USER1 role denied access
   - USER2/USER3 roles granted access
   - Unauthenticated user redirected to login

4. **Record Creation Tests**
   - New record creation
   - Existing record update (upsert)
   - Company association for admin users

### Property-Based Testing

Property-based tests will verify universal properties across all inputs using the **Hypothesis** library for Python:

**Configuration**: Each property test will run a minimum of 100 iterations.

**Test Tagging**: Each property-based test will include a comment with this format:
```python
# Feature: mandays-overtime-summary, Property X: [property description]
```

1. **Property 1: File format validation**
   - Generate random file objects with various extensions
   - Verify only CSV/XLS/XLSX are accepted

2. **Property 2: Mandatory column presence**
   - Generate CSV files with random subsets of columns
   - Verify files without all mandatory columns are rejected

3. **Property 3: Mandatory field validation**
   - Generate rows with random combinations of empty/null mandatory fields
   - Verify all such rows are rejected

4. **Property 4: Column extraction**
   - Generate CSV files with extra columns beyond the specified set
   - Verify only specified columns are extracted

5. **Property 5: Optional field handling**
   - Generate rows with random combinations of missing optional fields
   - Verify rows are accepted and NULL values stored

6. **Property 6: Numeric data type preservation**
   - Generate random decimal values for numeric fields
   - Verify values are stored with correct precision

7. **Property 7: Upload results reporting**
   - Generate random CSV files with mix of valid/invalid rows
   - Verify reported counts match actual processing results

8. **Property 8: Error detail reporting**
   - Generate rows with various validation errors
   - Verify each error includes row number and description

9. **Property 9: Date format validation**
   - Generate random dates in various formats
   - Verify valid formats accepted, invalid/future dates rejected

10. **Property 10: Numeric field validation**
    - Generate random numeric and non-numeric values
    - Verify only valid non-negative numbers accepted

11. **Property 11: Access control enforcement**
    - Generate requests from users with USER1 role
    - Verify all are denied access

12. **Property 12: Admin access grant**
    - Generate requests from users with USER2/USER3 roles
    - Verify all are granted access

13. **Property 13: Company data isolation**
    - Generate upload requests from various admin users
    - Verify all records associated with correct company

### Integration Testing

Integration tests will verify end-to-end workflows:

1. Complete upload workflow (file upload → processing → database storage)
2. List view with filtering and pagination
3. Export functionality with filtered data
4. Template download functionality

### Test Data Generators

For property-based testing, we will create generators for:
- Random CSV files with configurable columns
- Random employee numbers (alphanumeric strings)
- Random dates (past, present, future)
- Random decimal values (positive, negative, zero)
- Random user objects with different roles
- Random company objects

## Implementation Notes

### Performance Considerations

- Use bulk_create for batch inserts (similar to existing CSV processor)
- Implement progress tracking for large files
- Add database indexes on frequently queried fields
- Use select_related for foreign key queries to reduce database hits

### Security Considerations

- Validate file size before processing (10MB limit)
- Sanitize all user inputs
- Enforce role-based access control at view level
- Use Django's CSRF protection for all POST requests
- Log all upload operations for audit trail

### Reusability

The MandayProcessor class will follow the same pattern as CSVProcessor:
- Reusable validation methods
- Configurable field mappings
- Progress callback support
- Consistent error reporting format

### UI/UX Considerations

- Upload interface similar to existing attendance upload for consistency
- Clear error messages with actionable guidance
- Progress indicator for large file uploads
- Downloadable template file with correct headers
- Responsive design for mobile access
