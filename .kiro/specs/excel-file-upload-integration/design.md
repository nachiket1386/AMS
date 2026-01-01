# Design Document

## Overview

The Excel File Upload and Integration feature enables administrators and authorized users to upload Excel files containing attendance data and provides role-based access to view this data. The system automatically detects file types, validates data integrity, handles multiple Excel formats (HTML-based XLS, binary XLS, and XLSX), and imports records into a normalized database schema. Users can view data filtered by their role: employees see only their own records, contractors see all employees under their contractor code, and administrators have full access. The feature includes real-time progress tracking, comprehensive error reporting, import history logging, and data export capabilities.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Upload UI    │  │ Dashboard    │  │ Search/Filter│          │
│  │ - Drag/Drop  │  │ - Role-based │  │ - EP NO      │          │
│  │ - Preview    │  │ - Summary    │  │ - Date Range │          │
│  │ - Progress   │  │ - Charts     │  │ - Status     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                         API Layer (Django REST)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Upload API   │  │ Query API    │  │ Export API   │          │
│  │ - Validate   │  │ - Filter     │  │ - CSV        │          │
│  │ - Parse      │  │ - Paginate   │  │ - Excel      │          │
│  │ - Import     │  │ - Aggregate  │  │ - PDF        │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ File Parser  │  │ Validator    │  │ Importer     │          │
│  │ - Detect     │  │ - EP NO      │  │ - Bulk       │          │
│  │ - Parse HTML │  │ - Dates      │  │ - Relations  │          │
│  │ - Parse XLS  │  │ - Times      │  │ - Rollback   │          │
│  │ - Parse XLSX │  │ - Foreign    │  │ - Logging    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Permission   │  │ Query Builder│  │ Export       │          │
│  │ - Role Check │  │ - Filter     │  │ - Format     │          │
│  │ - Scope      │  │ - Join       │  │ - Stream     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Data Access Layer (ORM)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Models       │  │ Managers     │  │ Querysets    │          │
│  │ - Employee   │  │ - Bulk Ops   │  │ - Optimized  │          │
│  │ - Contractor │  │ - Validation │  │ - Prefetch   │          │
│  │ - PunchRec   │  │ - Filtering  │  │ - Annotate   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Database Layer (PostgreSQL)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Master Tables│  │ Transaction  │  │ Audit Tables │          │
│  │ - employees  │  │ - punch_rec  │  │ - import_log │          │
│  │ - contractors│  │ - overtime   │  │ - export_log │          │
│  │ - plants     │  │ - partial_day│  │ - error_log  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Frontend:** React.js with Material-UI components
- **Backend:** Django 4.x with Django REST Framework
- **Database:** PostgreSQL 14+
- **File Processing:** pandas, openpyxl, xlrd
- **Task Queue:** Celery with Redis (for async processing)
- **Storage:** Local filesystem or S3 for uploaded files
- **Authentication:** Django authentication with JWT tokens

## Components and Interfaces

### 1. File Upload Component

**Purpose:** Handle file selection, preview, and upload initiation

**Interface:**
```typescript
interface FileUploadProps {
  onUploadComplete: (result: UploadResult) => void;
  allowedFileTypes: string[];
  maxFileSize: number;
}

interface UploadResult {
  success: boolean;
  totalRows: number;
  importedRows: number;
  duplicates: number;
  errors: ValidationError[];
  importLogId: string;
}
```

**Key Methods:**
- `handleFileSelect(file: File): void` - Validate and preview file
- `detectFileType(columns: string[]): FileType` - Auto-detect file type
- `uploadFile(file: File, fileType: FileType): Promise<UploadResult>` - Upload and process

### 2. File Parser Service

**Purpose:** Parse different Excel formats and normalize data

**Interface:**
```python
class FileParserService:
    def parse_file(self, file_path: str) -> pd.DataFrame:
        """Parse Excel file and return DataFrame"""
        
    def detect_file_type(self, df: pd.DataFrame) -> FileType:
        """Detect file type based on columns"""
        
    def normalize_data(self, df: pd.DataFrame, file_type: FileType) -> pd.DataFrame:
        """Normalize column names and data formats"""
```

**Supported Formats:**
- HTML-based XLS (parsed with pandas.read_html)
- Binary XLS (parsed with xlrd)
- XLSX (parsed with openpyxl)

### 3. Data Validator Service

**Purpose:** Validate data integrity and business rules

**Interface:**
```python
class DataValidatorService:
    def validate_ep_no(self, ep_no: str) -> ValidationResult:
        """Validate EP NO format (PP\d{10} or VP\d{10})"""
        
    def validate_date(self, date_str: str) -> ValidationResult:
        """Validate and parse date in DD/MM/YYYY format"""
        
    def validate_time(self, time_str: str) -> ValidationResult:
        """Validate time in HH:MM or HH:MM:SS format"""
        
    def validate_foreign_keys(self, df: pd.DataFrame) -> List[ValidationError]:
        """Check contractor codes and other foreign keys exist"""
        
    def validate_batch(self, df: pd.DataFrame, file_type: FileType) -> ValidationReport:
        """Validate entire DataFrame and return report"""
```

**Validation Rules:**
- EP NO: Must match `^(PP|VP)\d{10}$`
- PUNCHDATE: Must be valid date, not future
- CONTRACTOR CODE: Must exist in contractors table
- Time fields: Must be valid HH:MM or HH:MM:SS
- Required fields: Must not be null

### 4. Data Importer Service

**Purpose:** Import validated data into database with transaction management

**Interface:**
```python
class DataImporterService:
    def import_batch(self, df: pd.DataFrame, file_type: FileType, user: User) -> ImportResult:
        """Import DataFrame into database with rollback on error"""
        
    def create_or_update_employees(self, df: pd.DataFrame) -> int:
        """Upsert employee records"""
        
    def create_or_update_contractors(self, df: pd.DataFrame) -> int:
        """Upsert contractor records"""
        
    def import_punch_records(self, df: pd.DataFrame) -> int:
        """Import punch records with duplicate detection"""
        
    def import_exception_records(self, df: pd.DataFrame, record_type: str) -> int:
        """Import overtime/partial day/regularization records"""
```

**Import Strategy:**
- Use bulk_create for performance
- Check duplicates before insert (EP NO + PUNCHDATE)
- Create foreign key records if missing
- Wrap in database transaction for atomicity

### 5. Permission Service

**Purpose:** Enforce role-based access control

**Interface:**
```python
class PermissionService:
    def can_upload(self, user: User, file_type: FileType) -> bool:
        """Check if user can upload specific file type"""
        
    def get_query_scope(self, user: User) -> Q:
        """Return Django Q object for filtering based on role"""
        
    def filter_queryset(self, queryset: QuerySet, user: User) -> QuerySet:
        """Apply role-based filtering to queryset"""
```

**Role Scopes:**
- **Employee:** EP NO = user.employee_id
- **Contractor:** CONTRACTOR CODE = user.contractor_code
- **Admin:** No restrictions

### 6. Dashboard Component

**Purpose:** Display role-based attendance summary

**Interface:**
```typescript
interface DashboardProps {
  user: User;
  dateRange: DateRange;
}

interface DashboardData {
  summary: AttendanceSummary;
  recentRecords: AttendanceRecord[];
  pendingRequests: Request[];
  charts: ChartData[];
}
```

**Key Features:**
- Summary cards (total days, present, absent, overtime)
- Recent attendance table
- Pending requests list
- Attendance trend chart

### 7. Search and Filter Component

**Purpose:** Enable users to search and filter attendance data

**Interface:**
```typescript
interface SearchFilterProps {
  onFilterChange: (filters: FilterCriteria) => void;
  availableFilters: FilterOption[];
}

interface FilterCriteria {
  epNo?: string;
  employeeName?: string;
  dateRange?: DateRange;
  status?: string[];
  contractorCode?: string;
}
```

### 8. Export Service

**Purpose:** Generate export files in various formats

**Interface:**
```python
class ExportService:
    def export_to_csv(self, queryset: QuerySet, filename: str) -> str:
        """Export queryset to CSV file"""
        
    def export_to_excel(self, queryset: QuerySet, filename: str) -> str:
        """Export queryset to Excel file"""
        
    def stream_export(self, queryset: QuerySet, format: str) -> Iterator:
        """Stream large exports to avoid memory issues"""
```

## Data Models

### Database Schema

```sql
-- Master Tables

CREATE TABLE employees (
    ep_no VARCHAR(12) PRIMARY KEY,
    ep_name VARCHAR(255) NOT NULL,
    contractor_code INTEGER REFERENCES contractors(contractor_code),
    sector_name VARCHAR(100),
    plant_name VARCHAR(100),
    department_name VARCHAR(100),
    trade_name VARCHAR(100),
    skill VARCHAR(50),
    card_category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contractors (
    contractor_code INTEGER PRIMARY KEY,
    contractor_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE plants (
    plant_code VARCHAR(50) PRIMARY KEY,
    plant_name VARCHAR(255) NOT NULL,
    sector_name VARCHAR(100),
    site_code VARCHAR(50),
    site_desc VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transaction Tables

CREATE TABLE punch_records (
    id SERIAL PRIMARY KEY,
    ep_no VARCHAR(12) REFERENCES employees(ep_no),
    punchdate DATE NOT NULL,
    shift VARCHAR(50),
    punch1_in TIME,
    punch2_out TIME,
    punch3_in TIME,
    punch4_out TIME,
    punch5_in TIME,
    punch6_out TIME,
    early_in TIME,
    late_come TIME,
    early_out TIME,
    hours_worked TIME,
    overstay TIME,
    overtime TIME,
    status VARCHAR(10),
    regular_hours TIME,
    manual_request BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ep_no, punchdate)
);

CREATE TABLE daily_summary (
    id SERIAL PRIMARY KEY,
    ep_no VARCHAR(12) REFERENCES employees(ep_no),
    punchdate DATE NOT NULL,
    mandays DECIMAL(5,2),
    regular_manday_hr TIME,
    ot DECIMAL(5,2),
    location_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ep_no, punchdate)
);

CREATE TABLE overtime_requests (
    id SERIAL PRIMARY KEY,
    ep_no VARCHAR(12) REFERENCES employees(ep_no),
    punchdate DATE NOT NULL,
    actual_overstay TIME,
    requested_overtime TIME,
    approved_overtime TIME,
    requested_regular_hours TIME,
    approved_regular_hours TIME,
    contractor_request_date TIMESTAMP,
    contractor_remarks TEXT,
    contractor_reason TEXT,
    actual_eic_code INTEGER,
    requested_eic_code INTEGER,
    eic_approve_date TIMESTAMP,
    eic_remarks TEXT,
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ep_no, punchdate)
);

CREATE TABLE partial_day_requests (
    id SERIAL PRIMARY KEY,
    ep_no VARCHAR(12) REFERENCES employees(ep_no),
    punchdate DATE NOT NULL,
    actual_pd_hours TIME,
    requested_pd_hours TIME,
    approved_pd_hours TIME,
    manday_conversion DECIMAL(3,2),
    contractor_request_date TIMESTAMP,
    contractor_remarks TEXT,
    eic_code INTEGER,
    eic_approve_date TIMESTAMP,
    eic_remarks TEXT,
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ep_no, punchdate)
);

CREATE TABLE regularization_requests (
    id SERIAL PRIMARY KEY,
    ep_no VARCHAR(12) REFERENCES employees(ep_no),
    punchdate DATE NOT NULL,
    old_punch_in TIME,
    old_punch_out TIME,
    new_punch_in TIME,
    new_punch_out TIME,
    contractor_request_date TIMESTAMP,
    contractor_remarks TEXT,
    contractor_reason TEXT,
    eic_code INTEGER,
    eic_approve_date TIMESTAMP,
    eic_remarks TEXT,
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ep_no, punchdate)
);

-- Audit Tables

CREATE TABLE import_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id),
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    total_rows INTEGER,
    imported_rows INTEGER,
    duplicate_rows INTEGER,
    error_rows INTEGER,
    status VARCHAR(20),
    error_report_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE export_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id),
    export_type VARCHAR(50),
    record_count INTEGER,
    filters JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE upload_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id),
    file_type VARCHAR(50),
    can_upload BOOLEAN DEFAULT FALSE,
    granted_by INTEGER REFERENCES auth_user(id),
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Django Models

```python
from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    ep_no = models.CharField(max_length=12, primary_key=True)
    ep_name = models.CharField(max_length=255)
    contractor = models.ForeignKey('Contractor', on_delete=models.PROTECT)
    sector_name = models.CharField(max_length=100, blank=True)
    plant_name = models.CharField(max_length=100, blank=True)
    department_name = models.CharField(max_length=100, blank=True)
    trade_name = models.CharField(max_length=100, blank=True)
    skill = models.CharField(max_length=50, blank=True)
    card_category = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'employees'
        indexes = [
            models.Index(fields=['contractor']),
            models.Index(fields=['plant_name']),
        ]

class Contractor(models.Model):
    contractor_code = models.IntegerField(primary_key=True)
    contractor_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contractors'

class PunchRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    punchdate = models.DateField()
    shift = models.CharField(max_length=50, blank=True)
    punch1_in = models.TimeField(null=True, blank=True)
    punch2_out = models.TimeField(null=True, blank=True)
    punch3_in = models.TimeField(null=True, blank=True)
    punch4_out = models.TimeField(null=True, blank=True)
    punch5_in = models.TimeField(null=True, blank=True)
    punch6_out = models.TimeField(null=True, blank=True)
    hours_worked = models.TimeField(null=True, blank=True)
    overstay = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'punch_records'
        unique_together = [['employee', 'punchdate']]
        indexes = [
            models.Index(fields=['punchdate']),
            models.Index(fields=['employee', 'punchdate']),
        ]

class ImportLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    total_rows = models.IntegerField()
    imported_rows = models.IntegerField()
    duplicate_rows = models.IntegerField()
    error_rows = models.IntegerField()
    status = models.CharField(max_length=20)
    error_report_path = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'import_logs'
        ordering = ['-created_at']
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: File extension validation
*For any* file selection, only files with .xls or .xlsx extensions should be accepted by the upload interface
**Validates: Requirements 1.2**

### Property 2: File type detection accuracy
*For any* Excel file with a valid column structure, the automatic file type detection should correctly identify the file type based on column names
**Validates: Requirements 1.3**

### Property 3: Preview row limit
*For any* uploaded file, the preview should contain exactly the minimum of 10 rows or the total number of rows in the file
**Validates: Requirements 1.4**

### Property 4: Complete row processing
*For any* uploaded file with valid data, all rows should be processed and valid records should be imported into the database
**Validates: Requirements 1.5**

### Property 5: EP NO format validation
*For any* EP NO value in an uploaded file, it should pass validation if and only if it matches the pattern ^(PP|VP)\d{10}$
**Validates: Requirements 2.1**

### Property 6: Date format validation
*For any* PUNCHDATE value in an uploaded file, it should pass validation if and only if it is a valid date in DD/MM/YYYY format and not a future date
**Validates: Requirements 2.2**

### Property 7: Foreign key validation
*For any* CONTRACTOR CODE in an uploaded file, it should pass validation if and only if a matching record exists in the contractors table
**Validates: Requirements 2.3**

### Property 8: Time format validation
*For any* time field value in an uploaded file, it should pass validation if and only if it matches HH:MM or HH:MM:SS format
**Validates: Requirements 2.4**

### Property 9: Error report completeness
*For any* uploaded file with validation errors, the generated error report should contain an entry for every invalid row with a specific error message
**Validates: Requirements 2.5**

### Property 10: Duplicate detection and logging
*For any* uploaded file containing records with duplicate primary keys (EP NO + PUNCHDATE), those duplicates should be skipped during import and logged in the import summary
**Validates: Requirements 2.7**

### Property 11: Import summary accuracy
*For any* completed upload operation, the summary counts (total rows, successful imports, duplicates, errors) should sum correctly and match the actual processing results
**Validates: Requirements 3.1**

### Property 12: Import log persistence
*For any* completed upload operation, an import log entry should exist in the database with all required fields (timestamp, filename, user, results)
**Validates: Requirements 3.2**

### Property 13: Transaction rollback on failure
*For any* upload operation that fails completely, no partial data should remain in the database after the rollback
**Validates: Requirements 3.5**

### Property 14: Employee data isolation
*For any* employee user viewing attendance data, only records where EP NO matches their employee ID should be visible
**Validates: Requirements 4.2**

### Property 15: Punch record field completeness
*For any* punch record displayed to a user, it should include all required fields: date, shift, punch times, hours worked, and status
**Validates: Requirements 4.3**

### Property 16: Request display completeness
*For any* employee viewing their requests, all overtime, partial day, and regularization requests should be displayed with their approval status
**Validates: Requirements 4.4**

### Property 17: Date range filtering accuracy
*For any* date range filter applied by a user, only records where PUNCHDATE falls within the selected range (inclusive) should be displayed
**Validates: Requirements 4.5, 5.5, 6.3**

### Property 18: Contractor data scope
*For any* contractor user viewing employee data, only employees where CONTRACTOR CODE matches their contractor code should be visible
**Validates: Requirements 5.2**

### Property 19: Pending request filtering
*For any* contractor viewing pending requests, only overtime, partial day, and regularization requests with status='Pending' for their employees should be displayed
**Validates: Requirements 5.4**

### Property 20: EP NO search with permissions
*For any* user searching by EP NO, all records matching that employee ID within the user's permission scope should be returned
**Validates: Requirements 6.1**

### Property 21: Name search with permissions
*For any* user searching by employee name, all records for employees with matching names within the user's permission scope should be returned
**Validates: Requirements 6.2**

### Property 22: Status filtering accuracy
*For any* status filter applied by a user, only records with the selected status value should be displayed
**Validates: Requirements 6.4**

### Property 23: Multiple filter combination
*For any* set of filters applied simultaneously, only records matching all filter criteria should be displayed (AND logic)
**Validates: Requirements 6.5**

### Property 24: Permission-based file type display
*For any* user with limited upload permissions accessing the upload interface, only file types they are authorized to upload should be displayed
**Validates: Requirements 7.3**

### Property 25: Data normalization consistency
*For any* successfully parsed file, all data should be normalized to consistent formats (dates, times, column names) before validation
**Validates: Requirements 8.5**

### Property 26: Employee upsert correctness
*For any* employee data in an uploaded file, if an employee with that EP NO exists, the record should be updated; otherwise, a new record should be created
**Validates: Requirements 9.1**

### Property 27: Contractor upsert correctness
*For any* contractor data in an uploaded file, if a contractor with that code exists, the record should be updated; otherwise, a new record should be created
**Validates: Requirements 9.2**

### Property 28: Foreign key integrity
*For any* imported punch record or exception record, all foreign key references (employee, contractor) should point to existing records in their respective tables
**Validates: Requirements 9.3, 9.4**

### Property 29: Missing foreign key resolution
*For any* record with a missing foreign key reference, the system should either create the referenced record (if data is available) or log a validation error
**Validates: Requirements 9.5**

### Property 30: Export data accuracy
*For any* filtered dataset exported to CSV, the exported file should contain exactly the records that match the applied filters with all column headers matching database field names
**Validates: Requirements 10.2, 10.3**

### Property 31: Export filename format
*For any* export operation, the generated filename should include the export date and time in a consistent format
**Validates: Requirements 10.4**

### Property 32: Export operation logging
*For any* export operation, a log entry should be created with user, timestamp, and record count
**Validates: Requirements 10.5**

## Error Handling

### Upload Errors

1. **File Format Errors:**
   - Invalid file extension → Display error: "Only .xls and .xlsx files are supported"
   - Corrupted file → Display error: "File is corrupted or in an unsupported format"
   - Empty file → Display error: "File contains no data"

2. **Validation Errors:**
   - Invalid EP NO → Log error: "Invalid EP NO format: {value}. Expected PP/VP followed by 10 digits"
   - Invalid date → Log error: "Invalid date format: {value}. Expected DD/MM/YYYY"
   - Future date → Log error: "Date cannot be in the future: {value}"
   - Invalid time → Log error: "Invalid time format: {value}. Expected HH:MM or HH:MM:SS"
   - Missing contractor → Log error: "Contractor code {code} does not exist"
   - Missing required field → Log error: "Required field {field} is missing or empty"

3. **Import Errors:**
   - Database connection failure → Rollback transaction, display error: "Database connection failed. Please try again"
   - Constraint violation → Rollback transaction, log error: "Database constraint violation: {details}"
   - Timeout → Rollback transaction, display error: "Import timed out. Please try with a smaller file"

### Query Errors

1. **Permission Errors:**
   - Unauthorized access → Display error: "You do not have permission to access this data"
   - Invalid role → Display error: "Invalid user role configuration"

2. **Search Errors:**
   - Invalid date range → Display error: "End date must be after start date"
   - No results found → Display message: "No records found matching your criteria"

### Export Errors

1. **Export Errors:**
   - Too many records → Display error: "Export size exceeds limit. Please apply filters to reduce the dataset"
   - File write failure → Display error: "Failed to generate export file. Please try again"

### Error Recovery

- All database operations wrapped in transactions
- Automatic rollback on any error during import
- Detailed error logging for debugging
- User-friendly error messages
- Error reports downloadable as CSV
- Retry mechanism for transient failures

## Testing Strategy

### Unit Testing

**File Parser Tests:**
- Test HTML XLS parsing with sample files
- Test binary XLS parsing with sample files
- Test XLSX parsing with sample files
- Test file type detection with various column structures
- Test data normalization for dates, times, column names

**Validator Tests:**
- Test EP NO validation with valid and invalid patterns
- Test date validation with various formats and edge cases
- Test time validation with various formats
- Test foreign key validation with existing and non-existing references
- Test batch validation with mixed valid/invalid data

**Importer Tests:**
- Test employee upsert with new and existing records
- Test contractor upsert with new and existing records
- Test punch record import with duplicates
- Test exception record import
- Test transaction rollback on errors

**Permission Tests:**
- Test role-based query scoping for employees
- Test role-based query scoping for contractors
- Test role-based query scoping for admins
- Test upload permission checks

**Export Tests:**
- Test CSV export with filtered data
- Test export filename generation
- Test export logging

### Property-Based Testing

The system will use **Hypothesis** (Python property-based testing library) to verify correctness properties. Each property test will run a minimum of 100 iterations with randomly generated data.

**Property Test Configuration:**
```python
from hypothesis import given, settings, strategies as st

@settings(max_examples=100)
@given(ep_no=st.from_regex(r'^(PP|VP)\d{10}$', fullmatch=True))
def test_ep_no_validation_accepts_valid_format(ep_no):
    """Property 5: EP NO format validation"""
    result = validator.validate_ep_no(ep_no)
    assert result.is_valid == True
```

**Test Data Generators:**
- EP NO generator: Valid and invalid patterns
- Date generator: Valid dates, invalid formats, future dates
- Time generator: Valid times, invalid formats
- Contractor code generator: Existing and non-existing codes
- File data generator: Complete datasets with various characteristics

### Integration Testing

**End-to-End Upload Flow:**
1. Upload file → Parse → Validate → Import → Verify database state
2. Upload with errors → Verify error report generation
3. Upload with duplicates → Verify duplicate detection and logging
4. Upload with missing foreign keys → Verify resolution or error logging

**Role-Based Access Flow:**
1. Employee login → View dashboard → Verify only own records visible
2. Contractor login → View employees → Verify only contractor's employees visible
3. Admin login → View all data → Verify no restrictions

**Search and Filter Flow:**
1. Apply EP NO filter → Verify results
2. Apply date range filter → Verify results
3. Apply multiple filters → Verify AND logic
4. Export filtered data → Verify export matches filters

### Performance Testing

**Load Testing:**
- Upload files with 10K, 50K, 100K rows
- Measure import time and memory usage
- Test concurrent uploads by multiple users
- Test query performance with large datasets

**Optimization Targets:**
- Import: < 1 second per 1000 rows
- Query: < 500ms for filtered results
- Export: < 2 seconds for 10K rows
- Dashboard load: < 1 second

### Security Testing

**Authentication Tests:**
- Test unauthorized access attempts
- Test session expiration
- Test role escalation attempts

**Input Validation Tests:**
- Test SQL injection in search fields
- Test XSS in file uploads
- Test path traversal in file operations

**Data Privacy Tests:**
- Verify employees cannot see other employees' data
- Verify contractors cannot see other contractors' data
- Verify audit logging captures all access

## Implementation Notes

### Performance Optimizations

1. **Bulk Operations:**
   - Use Django's `bulk_create()` for batch inserts
   - Use `bulk_update()` for batch updates
   - Batch size: 1000 records per operation

2. **Database Indexing:**
   - Index on (ep_no, punchdate) for fast lookups
   - Index on contractor_code for contractor queries
   - Index on punchdate for date range queries

3. **Query Optimization:**
   - Use `select_related()` for foreign key joins
   - Use `prefetch_related()` for reverse foreign keys
   - Use `only()` to fetch required fields only
   - Implement pagination for large result sets

4. **Caching:**
   - Cache contractor list (rarely changes)
   - Cache user permissions (invalidate on change)
   - Cache dashboard summaries (5-minute TTL)

5. **Async Processing:**
   - Use Celery for large file uploads (> 10K rows)
   - Send progress updates via WebSocket
   - Queue exports for background processing

### Security Considerations

1. **File Upload Security:**
   - Validate file size (max 50MB)
   - Scan for malware
   - Store uploaded files outside web root
   - Use unique filenames to prevent overwrites

2. **Data Access Security:**
   - Enforce role-based access at API level
   - Use Django's permission system
   - Log all data access for audit
   - Implement rate limiting on API endpoints

3. **SQL Injection Prevention:**
   - Use Django ORM (parameterized queries)
   - Validate all user inputs
   - Escape special characters in search

4. **XSS Prevention:**
   - Sanitize all user inputs
   - Use Content Security Policy headers
   - Escape output in templates

### Scalability Considerations

1. **Database Scaling:**
   - Use read replicas for queries
   - Partition large tables by date
   - Archive old data (> 2 years)

2. **Application Scaling:**
   - Stateless API design for horizontal scaling
   - Use load balancer for multiple app servers
   - Separate upload processing to dedicated workers

3. **Storage Scaling:**
   - Use object storage (S3) for uploaded files
   - Implement file retention policy
   - Compress old files

### Monitoring and Logging

1. **Application Metrics:**
   - Upload success/failure rate
   - Average import time
   - Query response times
   - Error rates by type

2. **Business Metrics:**
   - Daily upload count
   - Records imported per day
   - Active users by role
   - Most common validation errors

3. **Logging:**
   - Structured logging (JSON format)
   - Log levels: DEBUG, INFO, WARNING, ERROR
   - Log rotation and retention (30 days)
   - Centralized log aggregation

4. **Alerting:**
   - Alert on high error rates
   - Alert on slow queries (> 5 seconds)
   - Alert on failed uploads
   - Alert on unauthorized access attempts
