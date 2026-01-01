"""
File Parser Service for Excel File Upload Integration

This service handles parsing of different Excel formats (HTML XLS, binary XLS, XLSX)
and normalizes data for validation and import.
"""
import pandas as pd
from enum import Enum
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class FileType(Enum):
    """Enum for different file types"""
    PUNCHRECORD = "punchrecord"
    ARC_SUMMARY = "arc_summary"
    OVERTIME = "overtime"
    PARTIAL_DAY = "partial_day"
    REGULARIZATION = "regularization"
    UNKNOWN = "unknown"


class FileParserService:
    """Service for parsing Excel files and detecting file types"""
    
    # Column patterns for file type detection
    FILE_TYPE_PATTERNS = {
        FileType.PUNCHRECORD: [
            'EP NO', 'EP NAME', 'PUNCHDATE', 'PUNCH1 IN', 'PUNCH2 OUT',
            'HOURS WORKED', 'STATUS'
        ],
        FileType.ARC_SUMMARY: [
            'epNo', 'punchDate', 'contCode', 'mandays', 'ot', 'trade'
        ],
        FileType.OVERTIME: [
            'EP NO', 'PUNCHDATE', 'ACTUAL OVERSTAY', 'REQUESTED OVERTIME',
            'APPROVED OVERTIME', 'OT REQUEST STATUS'
        ],
        FileType.PARTIAL_DAY: [
            'EP NO', 'PUNCHDATE', 'ACTUAL PD HOURS', 'REQUESTED PD HOURS',
            'APPROVED PD HOURS', 'MANDAY CONVERSION', 'PD REQUEST STATUS'
        ],
        FileType.REGULARIZATION: [
            'EP NO', 'PUNCHDATE', 'OLD PUNCH IN', 'OLD PUNCH OUT',
            'NEW PUNCH IN', 'NEW PUNCH OUT', 'REQUEST STATUS'
        ]
    }
    
    def parse_file(self, file_path: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Parse Excel file and return DataFrame
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            Tuple of (DataFrame, error_message)
            If successful, returns (DataFrame, None)
            If failed, returns (None, error_message)
        """
        try:
            # Try parsing as HTML first (for .xls files that are actually HTML)
            if file_path.endswith('.xls'):
                try:
                    df = pd.read_html(file_path)[0]
                    logger.info(f"Successfully parsed {file_path} as HTML")
                    return df, None
                except Exception as html_error:
                    logger.debug(f"HTML parsing failed: {html_error}, trying binary format")
                    # Try binary XLS format
                    try:
                        df = pd.read_excel(file_path, engine='xlrd')
                        logger.info(f"Successfully parsed {file_path} as binary XLS")
                        return df, None
                    except Exception as xls_error:
                        error_msg = str(xls_error)
                        logger.error(f"Binary XLS parsing failed: {xls_error}")
                        
                        # Check if error indicates HTML content or corrupted file
                        if 'BOF record' in error_msg or '<div>' in error_msg or '<html>' in error_msg.lower():
                            return None, (
                                "The uploaded file appears to be an HTML file or is corrupted, not a valid Excel file. "
                                "Please ensure you are uploading a genuine Excel file (.xls or .xlsx). "
                                "If you downloaded this file from a website, it may have downloaded an error page instead of the actual file. "
                                "Try opening the file in Excel first to verify it's valid."
                            )
                        
                        return None, f"Failed to parse XLS file: {error_msg}"
            
            # Parse XLSX files
            elif file_path.endswith('.xlsx'):
                try:
                    df = pd.read_excel(file_path, engine='openpyxl')
                    logger.info(f"Successfully parsed {file_path} as XLSX")
                    return df, None
                except Exception as xlsx_error:
                    error_msg = str(xlsx_error)
                    logger.error(f"XLSX parsing failed: {xlsx_error}")
                    
                    # Check if error indicates HTML content or corrupted file
                    if '<div>' in error_msg or '<html>' in error_msg.lower() or 'not a zip file' in error_msg.lower():
                        return None, (
                            "The uploaded file appears to be corrupted or is not a valid Excel file. "
                            "Please verify the file is a genuine Excel file (.xlsx) and try again. "
                            "If you downloaded this file, try downloading it again. "
                            "Try opening the file in Excel first to verify it's valid."
                        )
                    
                    return None, f"Failed to parse XLSX file: {error_msg}"
            
            else:
                return None, "Unsupported file format. Only .xls and .xlsx files are supported."
                
        except Exception as e:
            logger.error(f"Unexpected error parsing file: {e}")
            return None, f"Unexpected error: {str(e)}"
    
    def detect_file_type(self, df: pd.DataFrame) -> FileType:
        """
        Detect file type based on column structure
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            FileType enum value
        """
        if df is None or df.empty:
            return FileType.UNKNOWN
        
        # Get column names (case-insensitive comparison)
        columns = [str(col).strip() for col in df.columns]
        columns_lower = [col.lower() for col in columns]
        
        # Check each file type pattern
        for file_type, required_columns in self.FILE_TYPE_PATTERNS.items():
            required_lower = [col.lower() for col in required_columns]
            
            # Check if all required columns are present
            matches = sum(1 for req_col in required_lower if any(req_col in col for col in columns_lower))
            
            # If at least 70% of required columns match, consider it a match
            if matches >= len(required_columns) * 0.7:
                logger.info(f"Detected file type: {file_type.value} ({matches}/{len(required_columns)} columns matched)")
                return file_type
        
        logger.warning(f"Could not detect file type. Columns: {columns}")
        return FileType.UNKNOWN
    
    def normalize_data(self, df: pd.DataFrame, file_type: FileType) -> pd.DataFrame:
        """
        Normalize data to consistent formats
        
        Args:
            df: DataFrame to normalize
            file_type: Detected file type
            
        Returns:
            Normalized DataFrame
        """
        if df is None or df.empty:
            return df
        
        # Make a copy to avoid modifying original
        df = df.copy()
        
        # Normalize column names
        df.columns = [self._normalize_column_name(col) for col in df.columns]
        
        # Normalize dates
        date_columns = ['punchdate', 'punch_date', 'date']
        for col in date_columns:
            if col in df.columns:
                df[col] = self._normalize_dates(df[col])
        
        # Normalize times
        time_columns = [col for col in df.columns if any(
            keyword in col.lower() for keyword in ['time', 'hours', 'overstay', 'overtime', 'in', 'out']
        )]
        for col in time_columns:
            if col in df.columns:
                df[col] = self._normalize_times(df[col])
        
        # Handle NaN values
        df = df.fillna('')
        
        logger.info(f"Normalized {len(df)} rows for file type {file_type.value}")
        return df
    
    def _normalize_column_name(self, col_name: str) -> str:
        """
        Normalize column name to consistent format
        
        Args:
            col_name: Original column name
            
        Returns:
            Normalized column name (lowercase, underscores)
        """
        # Convert to string and strip whitespace
        col_name = str(col_name).strip()
        
        # Replace spaces with underscores
        col_name = col_name.replace(' ', '_')
        
        # Convert to lowercase
        col_name = col_name.lower()
        
        return col_name
    
    def _normalize_dates(self, date_series: pd.Series) -> pd.Series:
        """
        Normalize dates to YYYY-MM-DD format
        
        Args:
            date_series: Series containing dates
            
        Returns:
            Normalized date series
        """
        try:
            # Try parsing with dayfirst=True for DD/MM/YYYY format
            return pd.to_datetime(date_series, dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')
        except Exception as e:
            logger.warning(f"Date normalization failed: {e}")
            return date_series
    
    def _normalize_times(self, time_series: pd.Series) -> pd.Series:
        """
        Normalize times to HH:MM:SS format, preserving (N) day indicators
        
        Supports formats: HH:MM, HH:MM:SS, HH:MM (N), HH:MM (N):SS
        
        Args:
            time_series: Series containing times
            
        Returns:
            Normalized time series
        """
        try:
            # Convert to string and handle various time formats
            def normalize_time(val):
                if pd.isna(val) or val == '':
                    return ''
                
                val_str = str(val).strip()
                
                # Handle "0" as valid empty value
                if val_str == '0' or val_str == '0.0':
                    return ''
                
                # Extract day indicator (N) if present
                day_indicator = ''
                clean_val = val_str
                if '(' in val_str and ')' in val_str:
                    # Extract the (N) part
                    start_idx = val_str.index('(')
                    end_idx = val_str.index(')') + 1
                    day_indicator = val_str[start_idx:end_idx]
                    # Remove (N) for time parsing
                    before_paren = val_str[:start_idx].strip()
                    after_paren = val_str[end_idx:].strip()
                    if after_paren.startswith(':'):
                        clean_val = before_paren + after_paren
                    else:
                        clean_val = before_paren
                
                # If already in HH:MM or HH:MM:SS format, normalize
                if ':' in clean_val:
                    parts = clean_val.split(':')
                    if len(parts) == 2:
                        normalized = f"{parts[0].zfill(2)}:{parts[1].zfill(2)}:00"
                    elif len(parts) == 3:
                        normalized = f"{parts[0].zfill(2)}:{parts[1].zfill(2)}:{parts[2].zfill(2)}"
                    else:
                        return val_str
                    
                    # Append day indicator if present
                    if day_indicator:
                        return f"{normalized} {day_indicator}"
                    return normalized
                
                return val_str
            
            return time_series.apply(normalize_time)
        except Exception as e:
            logger.warning(f"Time normalization failed: {e}")
            return time_series
    
    def get_preview_data(self, df: pd.DataFrame, num_rows: int = 10) -> pd.DataFrame:
        """
        Get preview of first N rows
        
        Args:
            df: DataFrame to preview
            num_rows: Number of rows to return (default 10)
            
        Returns:
            DataFrame with first N rows
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        return df.head(min(num_rows, len(df)))
