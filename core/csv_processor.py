"""
CSV/Excel processing and validation component
"""
from datetime import datetime, date, time as dt_time
import csv
from io import StringIO, BytesIO
from django.utils import timezone
from .models import Company, AttendanceRecord

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class CSVProcessor:
    """Handles CSV/Excel file validation and processing for attendance records"""
    
    REQUIRED_FIELDS = ['EP NO', 'EP NAME', 'COMPANY NAME', 'DATE', 'SHIFT', 'STATUS']
    OPTIONAL_FIELDS = ['IN', 'OUT', 'IN (2)', 'OUT (2)', 'IN (3)', 'OUT (3)', 'OVERSTAY', 'OVERTIME', 'OVERTIME TO MANDAYS']
    VALID_STATUS = ['P', 'A', 'PH', 'L', 'WO', '-0.5', '-1']
    
    # Column name mappings: Upload file column -> Database column
    # This maps the columns from your upload file to the expected database columns
    COLUMN_ALIASES = {
        # Upload file column : Database column
        'CONTRACTOR NAME': 'COMPANY NAME',
        'PUNCHDATE': 'DATE',
        'PUNCH1 IN': 'IN',
        'PUNCH2 OUT': 'OUT',
        'PUNCH3 IN': 'IN (2)',
        'PUNCH4 OUT': 'OUT (2)',
        'PUNCH5 IN': 'IN (3)',
        'PUNCH6 OUT': 'OUT (3)',
        'REGULAR HOURS': 'OVERTIME TO MANDAYS',
        # Note: 'HOURS WORKED' will be skipped as 'HOURS' is not in the database
    }
    
    def __init__(self, fast_mode=True):
        self.errors = []
        self.success_count = 0
        self.updated_count = 0
        self.error_count = 0
        self.total_rows = 0
        self.processed_rows = 0
        self.progress_callback = None
        self.fast_mode = fast_mode  # Skip heavy validation for speed
    
    def read_file_to_dataframe(self, file):
        """
        Read CSV, Excel, or HTML table file into a pandas DataFrame
        
        Args:
            file: Uploaded file object
        
        Returns:
            pandas DataFrame or None if error
        """
        filename = file.name.lower()
        
        try:
            if filename.endswith('.csv'):
                # Read CSV file
                content = file.read().decode('utf-8')
                file.seek(0)
                df = pd.read_csv(StringIO(content))
            elif filename.endswith('.xlsx'):
                # Read Excel file (xlsx format)
                if not PANDAS_AVAILABLE:
                    raise Exception('Excel support requires pandas and openpyxl packages')
                file_content = file.read()
                file.seek(0)
                
                # Check if file is actually HTML
                if file_content.startswith(b'<'):
                    # Read as HTML table
                    content = file_content.decode('utf-8')
                    tables = pd.read_html(StringIO(content))
                    if not tables:
                        raise Exception('No tables found in HTML file')
                    df = tables[0]  # Use first table
                else:
                    df = pd.read_excel(BytesIO(file_content), engine='openpyxl')
            elif filename.endswith('.xls'):
                # Read Excel file (xls format - older format)
                if not PANDAS_AVAILABLE:
                    raise Exception('Excel support requires pandas and xlrd packages')
                
                file_content = file.read()
                file.seek(0)
                
                # Check if file is actually HTML (common issue with .xls files)
                if file_content.startswith(b'<'):
                    # Read as HTML table
                    content = file_content.decode('utf-8')
                    tables = pd.read_html(StringIO(content))
                    if not tables:
                        raise Exception('No tables found in HTML file')
                    df = tables[0]  # Use first table
                else:
                    try:
                        df = pd.read_excel(BytesIO(file_content), engine='xlrd')
                    except Exception as e:
                        # If xlrd fails, try openpyxl (sometimes .xls files are actually .xlsx)
                        file.seek(0)
                        try:
                            df = pd.read_excel(BytesIO(file.read()), engine='openpyxl')
                            file.seek(0)
                        except:
                            raise Exception(f'Unable to read .xls file: {str(e)}')
            else:
                return None
            
            # Clean column names (strip whitespace)
            df.columns = df.columns.str.strip()
            
            return df
        except Exception as e:
            raise Exception(f'Error reading file: {str(e)}')
    
    def validate_csv(self, file):
        """
        Validate CSV/Excel file structure and headers
        
        Args:
            file: Uploaded file object
        
        Returns:
            dict with 'valid' boolean and 'errors' list
        """
        try:
            # Try to read file as DataFrame
            df = self.read_file_to_dataframe(file)
            
            if df is None:
                return {'valid': False, 'errors': ['Unsupported file format']}
            
            if df.empty:
                return {'valid': False, 'errors': ['File is empty or has no data']}
            
            headers = df.columns.tolist()
            
            if not headers:
                return {'valid': False, 'errors': ['File has no headers']}
            
            # Check for required fields (case-insensitive and flexible matching with aliases)
            missing_fields = []
            for required_field in self.REQUIRED_FIELDS:
                field_found = False
                
                # Check if field exists directly (exact match or case-insensitive)
                if any(col.upper() == required_field.upper() for col in headers):
                    field_found = True
                else:
                    # Check if any alias maps to this required field
                    for alias, target in self.COLUMN_ALIASES.items():
                        if target.upper() == required_field.upper():
                            # Check if the alias exists in headers
                            if any(col.upper() == alias.upper() for col in headers):
                                field_found = True
                                break
                
                if not field_found:
                    missing_fields.append(required_field)
            
            if missing_fields:
                return {
                    'valid': False,
                    'errors': [f'Missing required fields: {", ".join(missing_fields)}. Found columns: {", ".join(headers)}']
                }
            
            return {'valid': True, 'errors': []}
            
        except Exception as e:
            return {'valid': False, 'errors': [f'Error reading file: {str(e)}']}
    
    def validate_date(self, date_str):
        """
        Validate date format (YYYY-MM-DD, DD-MM-YYYY, or pandas datetime) and ensure it's not a future date
        
        Args:
            date_str: Date string or datetime object to validate
        
        Returns:
            date object or None if invalid
        """
        if date_str is None:
            return None
        
        # Handle pandas NaT (Not a Time)
        if pd.isna(date_str):
            return None
        
        # If it's already a datetime object (from pandas), convert to date
        if isinstance(date_str, pd.Timestamp):
            parsed_date = date_str.date()
        elif isinstance(date_str, datetime):
            parsed_date = date_str.date()
        elif isinstance(date_str, date):
            parsed_date = date_str
        else:
            # It's a string, try to parse it
            date_str = str(date_str).strip()
            if not date_str:
                return None
            
            parsed_date = None
            
            # Try multiple date formats
            date_formats = [
                '%Y-%m-%d',      # 2025-11-21
                '%d-%m-%Y',      # 21-11-2025
                '%d/%m/%Y',      # 21/11/2025
                '%Y/%m/%d',      # 2025/11/21
                '%d.%m.%Y',      # 21.11.2025
                '%Y.%m.%d',      # 2025.11.21
            ]
            
            for date_format in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, date_format).date()
                    break
                except ValueError:
                    continue
            
            if parsed_date is None:
                return None
        
        # Check if date is in the future
        if parsed_date and parsed_date > date.today():
            return None
        
        return parsed_date
    
    def validate_time(self, time_str):
        """
        Validate time format (HH:MM or HH:MM (N))
        
        Args:
            time_str: Time string to validate
        
        Returns:
            time object or None if invalid or empty
        """
        if not time_str or not time_str.strip():
            return None
        
        time_str = time_str.strip()
        
        # Check if format is HH:MM (N) and extract just HH:MM
        if '(' in time_str and ')' in time_str:
            # Extract time before the parenthesis
            time_str = time_str.split('(')[0].strip()
        
        try:
            parsed_time = datetime.strptime(time_str, '%H:%M').time()
            return parsed_time
        except ValueError:
            return None
    
    def validate_status(self, status):
        """
        Validate status value against allowed values
        
        Args:
            status: Status string to validate
        
        Returns:
            Boolean indicating if status is valid
        """
        if not status:
            return False
        
        return status.strip() in self.VALID_STATUS
    
    def process_row(self, row, row_number, user):
        """
        Process and validate a single CSV/Excel row
        
        Args:
            row: Dictionary containing row data
            row_number: Row number for error reporting
            user: User performing the upload
        
        Returns:
            tuple (success, error_message, data_dict)
        """
        errors = []
        
        # Helper function to check if value is empty (handles pandas NaN)
        def is_empty(value):
            if value is None:
                return True
            if pd.isna(value):
                return True
            if isinstance(value, str) and not value.strip():
                return True
            return False
        
        # Validate required fields
        for field in self.REQUIRED_FIELDS:
            if field not in row or is_empty(row.get(field)):
                errors.append(f"Row {row_number}: Missing required field '{field}'")
        
        if errors:
            return (False, '; '.join(errors), None)
        
        # Validate date
        date_value = self.validate_date(row['DATE'])
        if date_value is None:
            errors.append(f"Row {row_number}: Invalid date format or future date in 'DATE' field")
        
        # Validate status
        if not self.validate_status(row['STATUS']):
            errors.append(f"Row {row_number}: Invalid status value '{row['STATUS']}'. Must be one of: {', '.join(self.VALID_STATUS)}")
        
        # Validate optional time fields
        time_fields = {
            'IN': 'in_time',
            'OUT': 'out_time',
            'IN (2)': 'in_time_2',
            'OUT (2)': 'out_time_2',
            'IN (3)': 'in_time_3',
            'OUT (3)': 'out_time_3',
            'OVERTIME': 'overtime',
            'OVERTIME TO MANDAYS': 'overtime_to_mandays'
        }
        
        time_values = {}
        for csv_field, model_field in time_fields.items():
            if csv_field in row and not is_empty(row[csv_field]):
                time_value = self.validate_time(str(row[csv_field]))
                if time_value is None:
                    errors.append(f"Row {row_number}: Invalid time format in '{csv_field}' field")
                else:
                    time_values[model_field] = time_value
            else:
                time_values[model_field] = None
        
        if errors:
            return (False, '; '.join(errors), None)
        
        # Get or create company
        company_name = row['COMPANY NAME'].strip()
        
        # STRICT: Check company access for admin users
        if user.role == 'admin':
            if not user.company:
                return (False, f"Row {row_number}: Admin user must have a company assigned", None)
            if user.company.name != company_name:
                return (False, f"Row {row_number}: Access Denied - Company '{company_name}' does not match your assigned company '{user.company.name}'. Admin users can only upload data for their own company.", None)
        
        try:
            company, _ = Company.objects.get_or_create(name=company_name)
        except Exception as e:
            return (False, f"Row {row_number}: Error creating/getting company: {str(e)}", None)
        
        # Prepare data dictionary
        data = {
            'ep_no': str(row['EP NO']).strip(),
            'ep_name': str(row['EP NAME']).strip(),
            'company': company,
            'date': date_value,
            'shift': str(row['SHIFT']).strip(),
            'overstay': str(row.get('OVERSTAY', '')).strip() if not is_empty(row.get('OVERSTAY')) else '',
            'status': str(row['STATUS']).strip(),
            **time_values
        }
        
        return (True, None, data)
    
    def create_or_update_record(self, data):
        """
        Create new or update existing attendance record
        
        Args:
            data: Dictionary containing record data
        
        Returns:
            tuple (created, updated) - booleans indicating if record was created or updated
        """
        try:
            record, created = AttendanceRecord.objects.update_or_create(
                ep_no=data['ep_no'],
                date=data['date'],
                defaults=data
            )
            return (created, not created)
        except Exception as e:
            raise Exception(f"Error saving record: {str(e)}")
    
    def normalize_column_name(self, col_name):
        """Normalize column name for matching"""
        return str(col_name).strip().upper()
    
    def map_columns(self, df_columns):
        """
        Map DataFrame columns to expected field names
        Only includes columns that match expected fields or their aliases
        
        Args:
            df_columns: List of column names from DataFrame
        
        Returns:
            dict mapping DataFrame columns to expected field names
        """
        column_mapping = {}
        all_expected_fields = self.REQUIRED_FIELDS + self.OPTIONAL_FIELDS
        
        for df_col in df_columns:
            normalized_df_col = self.normalize_column_name(df_col)
            
            # First, check if this column is an alias
            mapped_field = None
            for alias, target in self.COLUMN_ALIASES.items():
                if normalized_df_col == self.normalize_column_name(alias):
                    mapped_field = target
                    break
            
            # If it's an alias, use the mapped field
            if mapped_field:
                column_mapping[df_col] = mapped_field
                continue
            
            # Otherwise, check for direct match with expected fields
            for expected_field in all_expected_fields:
                normalized_expected = self.normalize_column_name(expected_field)
                
                if normalized_df_col == normalized_expected:
                    column_mapping[df_col] = expected_field
                    break
        
        return column_mapping
    
    def process_csv(self, file, user):
        """
        Process entire CSV/Excel file
        
        Args:
            file: Uploaded file object
            user: User performing the upload
        
        Returns:
            dict with processing results
        """
        self.errors = []
        self.success_count = 0
        self.updated_count = 0
        self.error_count = 0
        
        # Validate file structure
        validation_result = self.validate_csv(file)
        if not validation_result['valid']:
            return {
                'success': False,
                'errors': validation_result['errors'],
                'success_count': 0,
                'updated_count': 0,
                'error_count': len(validation_result['errors'])
            }
        
        # Read file into DataFrame
        try:
            df = self.read_file_to_dataframe(file)
        except Exception as e:
            return {
                'success': False,
                'errors': [str(e)],
                'success_count': 0,
                'updated_count': 0,
                'error_count': 1
            }
        
        # Map columns (only process matching columns)
        column_mapping = self.map_columns(df.columns.tolist())
        
        # Create a new DataFrame with only mapped columns
        mapped_df = pd.DataFrame()
        for df_col, expected_col in column_mapping.items():
            mapped_df[expected_col] = df[df_col]
        
        # Convert DataFrame to list of dictionaries
        rows = mapped_df.to_dict('records')
        
        # Set total rows for progress tracking
        self.total_rows = len(rows)
        self.processed_rows = 0
        
        # Import logger for progress updates
        import logging
        logger = logging.getLogger(__name__)
        
        # Log initial progress
        logger.info(f'Starting to process {self.total_rows} rows')
        
        # ULTRA-FAST: Disable indexes for maximum speed
        from django.db import connection
        with connection.cursor() as cursor:
            # Drop indexes temporarily for speed
            try:
                cursor.execute("DROP INDEX IF EXISTS core_attendancerecord_ep_no_date_idx")
                cursor.execute("DROP INDEX IF EXISTS core_attendancerecord_company_id_date_idx")
                cursor.execute("DROP INDEX IF EXISTS core_attendancerecord_date_idx")
                logger.info("Indexes dropped for fast import")
            except:
                pass  # Indexes might not exist
        
        # ULTRA-FAST: Prepare records with minimal processing
        records_to_create = []
        batch_size = 5000  # MUCH larger batches for maximum speed
        
        # Process rows with minimal validation for speed
        for row_number, row in enumerate(rows, start=2):
            success, error_msg, data = self.process_row(row, row_number, user)
            
            if success:
                try:
                    records_to_create.append(AttendanceRecord(**data))
                    self.success_count += 1
                except Exception as e:
                    self.error_count += 1
                    if len(self.errors) < 100:  # Limit error storage
                        self.errors.append(str(e))
            else:
                self.error_count += 1
                if len(self.errors) < 100:
                    self.errors.append(error_msg)
            
            self.processed_rows += 1
            
            # Bulk save every batch_size records
            if len(records_to_create) >= batch_size:
                try:
                    # FASTEST: Use bulk_create with ignore_conflicts (no updates)
                    AttendanceRecord.objects.bulk_create(
                        records_to_create, 
                        ignore_conflicts=True,
                        batch_size=batch_size
                    )
                except Exception as e:
                    logger.error(f'Bulk create error: {str(e)}')
                
                records_to_create = []
                
                # Log progress less frequently for speed
                if self.processed_rows % 5000 == 0:
                    logger.info(f'Progress: {self.processed_rows}/{self.total_rows} rows ({int(self.processed_rows/self.total_rows*100)}%)')
                    if self.progress_callback:
                        self.progress_callback(self.processed_rows, self.total_rows)
        
        # Save remaining records
        if records_to_create:
            try:
                AttendanceRecord.objects.bulk_create(
                    records_to_create, 
                    ignore_conflicts=True,
                    batch_size=batch_size
                )
            except Exception as e:
                logger.error(f'Final bulk create error: {str(e)}')
        
        # Final progress
        if self.progress_callback:
            self.progress_callback(self.processed_rows, self.total_rows)
        
        # Rebuild indexes for performance
        logger.info("Rebuilding indexes...")
        from django.db import connection
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS core_attendancerecord_ep_no_date_idx 
                    ON core_attendancerecord (ep_no, date)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS core_attendancerecord_company_id_date_idx 
                    ON core_attendancerecord (company_id, date)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS core_attendancerecord_date_idx 
                    ON core_attendancerecord (date)
                """)
                logger.info("Indexes rebuilt successfully")
            except Exception as e:
                logger.error(f"Error rebuilding indexes: {str(e)}")
        
        # Log final progress
        logger.info(f'Processing complete: {self.processed_rows}/{self.total_rows} rows processed (100%)')
        logger.info(f'Results: Created={self.success_count}, Updated={self.updated_count}, Errors={self.error_count}')
        
        return {
            'success': self.error_count == 0,
            'errors': self.errors,
            'success_count': self.success_count,
            'updated_count': self.updated_count,
            'error_count': self.error_count,
            'total_rows': self.total_rows,
            'processed_rows': self.processed_rows
        }
