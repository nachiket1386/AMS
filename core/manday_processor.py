"""
Manday CSV/Excel processing and validation component
"""
from datetime import datetime, date, time
from decimal import Decimal, InvalidOperation
from io import StringIO, BytesIO
from django.utils import timezone
from .models import Company, MandaySummaryRecord
import logging

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Get logger
logger = logging.getLogger(__name__)


class MandayProcessor:
    """Handles CSV/Excel file validation and processing for manday summary records"""
    
    REQUIRED_FIELDS = ['epNo', 'punchDate', 'mandays', 'regularMandayHr', 'ot']
    OPTIONAL_FIELDS = ['trade', 'contract', 'plant', 'plantDesc']
    
    # Column name mappings: Upload file column -> Expected column
    COLUMN_ALIASES = {
        'EP NO': 'epNo',
        'EP_NO': 'epNo',
        'EPNO': 'epNo',
        'PUNCH DATE': 'punchDate',
        'PUNCH_DATE': 'punchDate',
        'PUNCHDATE': 'punchDate',
        'MANDAYS': 'mandays',
        'MAN DAYS': 'mandays',
        'REGULAR MANDAY HR': 'regularMandayHr',
        'REGULAR_MANDAY_HR': 'regularMandayHr',
        'REGULARMANDAYHR': 'regularMandayHr',
        'OT': 'ot',
        'OVERTIME': 'ot',
        'TRADE': 'trade',
        'CONTRACT': 'contract',
        'PLANT': 'plant',
        'PLANT DESC': 'plantDesc',
        'PLANT_DESC': 'plantDesc',
        'PLANTDESC': 'plantDesc',
    }
    
    def __init__(self):
        self.errors = []
        self.success_count = 0
        self.updated_count = 0
        self.error_count = 0
        self.total_rows = 0
        self.processed_rows = 0
        self.progress_callback = None
    
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
        Validate date format and ensure it's not a future date
        
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
                '%m/%d/%Y',      # 11/21/2025 (US format)
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
    
    def validate_time_to_decimal(self, value, field_name):
        """
        Validate time value in HH:MM format and convert to decimal hours
        
        Args:
            value: Value to validate (can be HH:MM format or decimal)
            field_name: Name of field for error reporting
        
        Returns:
            Decimal object representing hours or None if invalid
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        
        # Handle pandas NaN
        if pd.isna(value):
            return None
        
        value_str = str(value).strip()
        
        # Check if it's in HH:MM format
        if ':' in value_str:
            try:
                parts = value_str.split(':')
                if len(parts) != 2:
                    return None
                
                hours = int(parts[0])
                minutes = int(parts[1])
                
                # Validate ranges
                if hours < 0 or minutes < 0 or minutes >= 60:
                    return None
                
                # Convert to decimal hours
                decimal_hours = Decimal(hours) + (Decimal(minutes) / Decimal(60))
                return decimal_hours
            except (ValueError, InvalidOperation):
                return None
        else:
            # Try to parse as decimal
            try:
                decimal_value = Decimal(value_str)
                
                # Check if value is negative
                if decimal_value < 0:
                    return None
                
                return decimal_value
            except (ValueError, InvalidOperation, TypeError):
                return None
    
    def decimal_hours_to_time(self, decimal_hours):
        """
        Convert decimal hours to time object
        
        Args:
            decimal_hours: Decimal representing hours
        
        Returns:
            time object or None if invalid
        """
        if decimal_hours is None:
            return None
        
        try:
            # Convert to float for calculation
            total_hours = float(decimal_hours)
            
            # Extract hours and minutes
            hours = int(total_hours)
            minutes = int((total_hours - hours) * 60)
            
            # Handle edge case where rounding might give 60 minutes
            if minutes >= 60:
                hours += 1
                minutes = 0
            
            # Validate ranges (time object only supports 0-23 hours)
            if hours < 0 or hours > 23 or minutes < 0 or minutes >= 60:
                return None
            
            return time(hour=hours, minute=minutes)
        except (ValueError, OverflowError):
            return None
    
    def validate_decimal(self, value, field_name):
        """
        Validate decimal/numeric value
        
        Args:
            value: Value to validate
            field_name: Name of field for error reporting
        
        Returns:
            Decimal object or None if invalid
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        
        # Handle pandas NaN
        if pd.isna(value):
            return None
        
        try:
            decimal_value = Decimal(str(value))
            
            # Check if value is negative
            if decimal_value < 0:
                return None
            
            return decimal_value
        except (ValueError, InvalidOperation, TypeError):
            return None
    
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
        date_value = self.validate_date(row['punchDate'])
        if date_value is None:
            errors.append(f"Row {row_number}: Invalid date format or future date in 'punchDate' field")
        
        # Validate numeric fields
        mandays_value = self.validate_decimal(row['mandays'], 'mandays')
        if mandays_value is None:
            errors.append(f"Row {row_number}: Invalid or negative value in 'mandays' field")
        
        # Validate regularMandayHr - can be in HH:MM format or decimal
        regular_hr_value = self.validate_time_to_decimal(row['regularMandayHr'], 'regularMandayHr')
        if regular_hr_value is None:
            errors.append(f"Row {row_number}: Invalid value in 'regularMandayHr' field (expected HH:MM format or decimal number)")
        
        # Validate ot - decimal number only
        ot_value = self.validate_decimal(row['ot'], 'ot')
        if ot_value is None:
            errors.append(f"Row {row_number}: Invalid or negative value in 'ot' field")
        
        if errors:
            return (False, '; '.join(errors), None)
        
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
        
        # Convert decimal hours to time object for regularMandayHr
        regular_hr_time = self.decimal_hours_to_time(regular_hr_value)
        if regular_hr_time is None:
            errors.append(f"Row {row_number}: Unable to convert 'regularMandayHr' to time format")
        
        if errors:
            return (False, '; '.join(errors), None)
        
        # Prepare data dictionary
        data = {
            'ep_no': str(row['epNo']).strip(),
            'punch_date': date_value,
            'mandays': mandays_value,
            'regular_manday_hr': regular_hr_time,
            'ot': ot_value,
            'company': company,
            # Optional fields
            'trade': str(row.get('trade', '')).strip() if not is_empty(row.get('trade')) else None,
            'contract': str(row.get('contract', '')).strip() if not is_empty(row.get('contract')) else None,
            'plant': str(row.get('plant', '')).strip() if not is_empty(row.get('plant')) else None,
            'plant_desc': str(row.get('plantDesc', '')).strip() if not is_empty(row.get('plantDesc')) else None,
        }
        
        return (True, None, data)
    
    def create_or_update_record(self, data):
        """
        Create new or update existing manday record
        
        Args:
            data: Dictionary containing record data
        
        Returns:
            tuple (created, updated) - booleans indicating if record was created or updated
        """
        try:
            # Convert decimal hours to time object for regular_manday_hr if needed
            if 'regular_manday_hr' in data and isinstance(data['regular_manday_hr'], Decimal):
                data['regular_manday_hr'] = self.decimal_hours_to_time(data['regular_manday_hr'])
            
            record, created = MandaySummaryRecord.objects.update_or_create(
                ep_no=data['ep_no'],
                punch_date=data['punch_date'],
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
                'error_count': len(validation_result['errors']),
                'total_rows': 0,
                'processed_rows': 0
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
                'error_count': 1,
                'total_rows': 0,
                'processed_rows': 0
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
        logger.info(f'Starting to process {self.total_rows} manday rows')
        
        # Process rows
        records_to_create = []
        batch_size = 1000
        
        for row_number, row in enumerate(rows, start=2):
            success, error_msg, data = self.process_row(row, row_number, user)
            
            if success:
                try:
                    created, updated = self.create_or_update_record(data)
                    if created:
                        self.success_count += 1
                    else:
                        self.updated_count += 1
                except Exception as e:
                    self.error_count += 1
                    if len(self.errors) < 100:  # Limit error storage
                        self.errors.append(str(e))
            else:
                self.error_count += 1
                if len(self.errors) < 100:
                    self.errors.append(error_msg)
            
            self.processed_rows += 1
            
            # Log progress
            if self.processed_rows % 1000 == 0:
                logger.info(f'Progress: {self.processed_rows}/{self.total_rows} rows ({int(self.processed_rows/self.total_rows*100)}%)')
                if self.progress_callback:
                    self.progress_callback(self.processed_rows, self.total_rows)
        
        # Final progress
        if self.progress_callback:
            self.progress_callback(self.processed_rows, self.total_rows)
        
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
