"""
Data Importer Service for Excel File Upload Integration

This service imports validated data into the database with transaction management.
"""
import pandas as pd
from django.db import transaction
from django.core.cache import cache
from typing import Dict, List, Tuple, Callable, Optional
from dataclasses import dataclass
import logging

from core.models import (
    Employee, Contractor, Plant,
    PunchRecord, DailySummary, OvertimeRequest, PartialDayRequest, RegularizationRequest,
    ImportLog, User
)
from core.services.file_parser_service import FileType

logger = logging.getLogger(__name__)


@dataclass
class ImportResult:
    """Result of an import operation"""
    success: bool
    total_rows: int
    imported_rows: int
    duplicate_rows: int
    error_rows: int
    error_message: str = ""
    import_log_id: int = None


@dataclass
class ImportProgress:
    """Progress information for an import operation"""
    total_rows: int
    processed_rows: int
    imported_rows: int
    duplicate_rows: int
    current_ep: str = ""
    status: str = "processing"  # processing, completed, error


class DataImporterService:
    """Service for importing validated data into database"""
    
    BATCH_SIZE = 1000  # Number of records to process in each batch
    
    def __init__(self):
        """Initialize importer service"""
        pass
    
    def _update_progress(self, session_id: str, progress: ImportProgress):
        """
        Update import progress in cache for real-time tracking
        
        Args:
            session_id: Session ID for this import
            progress: Progress information
        """
        cache_key = f"import_progress_{session_id}"
        cache.set(cache_key, {
            'total_rows': progress.total_rows,
            'processed_rows': progress.processed_rows,
            'imported_rows': progress.imported_rows,
            'duplicate_rows': progress.duplicate_rows,
            'current_ep': progress.current_ep,
            'status': progress.status
        }, timeout=300)  # 5 minutes
    
    def get_progress(self, session_id: str) -> Optional[Dict]:
        """
        Get current import progress
        
        Args:
            session_id: Session ID for this import
            
        Returns:
            Progress dictionary or None
        """
        cache_key = f"import_progress_{session_id}"
        return cache.get(cache_key)
    
    @transaction.atomic
    def import_batch(self, df: pd.DataFrame, file_type: FileType, user: User, filename: str, session_id: str = None) -> ImportResult:
        """
        Import DataFrame into AttendanceRecord model with rollback on error
        
        Args:
            df: DataFrame to import
            file_type: Type of file being imported
            user: User performing the import
            filename: Name of the uploaded file
            session_id: Optional session ID for progress tracking
            
        Returns:
            ImportResult with statistics
        """
        from core.models import AttendanceRecord, Company
        
        try:
            # Create import log entry
            import_log = ImportLog.objects.create(
                user=user,
                filename=filename,
                file_type=file_type.value,
                total_rows=len(df),
                imported_rows=0,
                duplicate_rows=0,
                error_rows=0,
                status='processing'
            )
            
            # Initialize progress tracking
            if session_id:
                progress = ImportProgress(
                    total_rows=len(df),
                    processed_rows=0,
                    imported_rows=0,
                    duplicate_rows=0,
                    status='processing'
                )
                self._update_progress(session_id, progress)
            
            # Import directly to AttendanceRecord with progress tracking
            imported_count, duplicate_count = self.import_attendance_records(df, user, session_id)
            
            # Update import log
            import_log.imported_rows = imported_count
            import_log.duplicate_rows = duplicate_count
            import_log.error_rows = len(df) - imported_count - duplicate_count
            import_log.status = 'completed'
            import_log.save()
            
            # Update final progress
            if session_id:
                progress.processed_rows = len(df)
                progress.imported_rows = imported_count
                progress.duplicate_rows = duplicate_count
                progress.status = 'completed'
                self._update_progress(session_id, progress)
            
            logger.info(f"Import completed: {imported_count} imported, {duplicate_count} duplicates")
            
            return ImportResult(
                success=True,
                total_rows=len(df),
                imported_rows=imported_count,
                duplicate_rows=duplicate_count,
                error_rows=0,
                import_log_id=import_log.id
            )
            
        except Exception as e:
            logger.error(f"Import failed: {e}")
            
            # Update error progress
            if session_id:
                progress = ImportProgress(
                    total_rows=len(df),
                    processed_rows=0,
                    imported_rows=0,
                    duplicate_rows=0,
                    status='error'
                )
                self._update_progress(session_id, progress)
            
            # Transaction will be rolled back automatically
            return ImportResult(
                success=False,
                total_rows=len(df),
                imported_rows=0,
                duplicate_rows=0,
                error_rows=len(df),
                error_message=str(e)
            )
    
    def import_attendance_records(self, df: pd.DataFrame, user: User, session_id: str = None) -> Tuple[int, int]:
        """
        Import attendance records to AttendanceRecord model with progress tracking
        
        Args:
            df: DataFrame containing attendance data
            user: User performing the import
            session_id: Optional session ID for progress tracking
            
        Returns:
            Tuple of (imported_count, duplicate_count)
        """
        from core.models import AttendanceRecord, Company
        
        # Column mappings
        ep_col = self._find_column(df, ['ep_no', 'ep no', 'epno'])
        name_col = self._find_column(df, [
            'ep_name', 'ep name', 'epname', 
            'employee_name', 'employee name', 'employeename',
            'name', 'empname', 'emp_name', 'emp name',
            'worker_name', 'worker name', 'workername',
            'full_name', 'full name', 'fullname'
        ])
        company_col = self._find_column(df, ['contractor_name', 'contractor name', 'company_name', 'company name', 'contractor_code', 'contractor code', 'cont_code', 'contcode'])
        date_col = self._find_column(df, ['punchdate', 'punch_date', 'date'])
        shift_col = self._find_column(df, ['shift'])
        status_col = self._find_column(df, ['status'])
        
        # ARC Summary specific columns
        trade_col = self._find_column(df, ['trade'])
        contract_col = self._find_column(df, ['contract'])
        mandays_col = self._find_column(df, ['mandays'])
        regular_hr_col = self._find_column(df, ['regular_manday_hr', 'regularmandayhr', 'regular manday hr'])
        ot_col = self._find_column(df, ['ot'])
        
        if not ep_col or not date_col:
            logger.error("Missing required columns: EP_NO or DATE")
            return 0, 0
        
        imported = 0
        duplicates = 0
        total_rows = len(df)
        
        for idx, row in df.iterrows():
            ep_no = row.get(ep_col)
            punchdate = row.get(date_col)
            
            # Update progress every 10 rows or on first/last row
            if session_id and (idx % 10 == 0 or idx == 0 or idx == total_rows - 1):
                progress = ImportProgress(
                    total_rows=total_rows,
                    processed_rows=idx + 1,
                    imported_rows=imported,
                    duplicate_rows=duplicates,
                    current_ep=str(ep_no) if pd.notna(ep_no) else "",
                    status='processing'
                )
                self._update_progress(session_id, progress)
            
            if pd.notna(ep_no) and pd.notna(punchdate):
                try:
                    # Parse date
                    if isinstance(punchdate, str):
                        punchdate = pd.to_datetime(punchdate).date()
                    elif isinstance(punchdate, pd.Timestamp):
                        punchdate = punchdate.date()
                    
                    # Get company
                    company_name = row.get(company_col, 'Unknown') if company_col else 'Unknown'
                    if pd.notna(company_name):
                        company_name = str(company_name).strip()
                    else:
                        company_name = 'Unknown'
                    
                    # Check company access for admin users
                    if user.role == 'admin':
                        if not user.company:
                            logger.warning(f"Admin user {user.username} has no company assigned")
                            continue
                        if user.company.name != company_name:
                            logger.warning(f"Access denied: Company '{company_name}' does not match admin's company '{user.company.name}'")
                            continue
                    
                    company, _ = Company.objects.get_or_create(name=company_name)
                    
                    # Prepare record data
                    record_data = {
                        'ep_name': str(row.get(name_col, f'Employee {ep_no}')) if name_col else f'Employee {ep_no}',
                        'company': company,
                        'shift': str(row.get(shift_col, '')) if shift_col and pd.notna(row.get(shift_col)) else '',
                        'status': str(row.get(status_col, 'P')) if status_col and pd.notna(row.get(status_col)) else 'P',
                        'overstay': '',
                    }
                    
                    # Add ARC Summary specific fields
                    if company_col:
                        record_data['cont_code'] = str(company_name)
                    if trade_col and pd.notna(row.get(trade_col)):
                        record_data['trade'] = str(row.get(trade_col))
                    if contract_col and pd.notna(row.get(contract_col)):
                        record_data['contract'] = str(row.get(contract_col))
                    if mandays_col and pd.notna(row.get(mandays_col)):
                        try:
                            record_data['mandays'] = float(row.get(mandays_col))
                        except (ValueError, TypeError):
                            pass
                    if regular_hr_col and pd.notna(row.get(regular_hr_col)):
                        record_data['regular_manday_hr'] = str(row.get(regular_hr_col))
                    if ot_col and pd.notna(row.get(ot_col)):
                        record_data['ot'] = str(row.get(ot_col))
                    
                    # Add Overtime request specific fields
                    ot_fields = {
                        'actual_overstay': ['actual_overstay', 'actual overstay', 'actualoverstay'],
                        'requested_overtime': ['requested_overtime', 'requested overtime', 'requestedovertime'],
                        'approved_overtime': ['approved_overtime', 'approved overtime', 'approvedovertime'],
                        'requested_regular_manday_hours': ['requested_regular_manday_hours', 'requested regular manday hours'],
                        'approved_regular_manday_hours': ['approved_regular_manday_hours', 'approved regular manday hours'],
                        'contractor_ot_remarks': ['contractor_ot_remarks', 'contractor ot remarks', 'ot remarks'],
                        'contractor_ot_reason': ['contractor_ot_reason', 'contractor ot reason', 'ot reason'],
                        'requested_eic_code': ['requested_eic_code', 'requested eic code', 'eic code'],
                        'requested_eic_name': ['requested_eic_name', 'requested eic name', 'eic name'],
                        'ot_request_status': ['ot_request_status', 'ot request status', 'request status'],
                    }
                    
                    for field_name, possible_cols in ot_fields.items():
                        col = self._find_column(df, possible_cols)
                        if col and pd.notna(row.get(col)):
                            record_data[field_name] = str(row.get(col))
                    
                    # Parse time fields with support for (N) indicator and hours > 24
                    time_field_mappings = {
                        'punch1_in': ['punch1 in', 'punch1_in', 'in', 'in_time'],
                        'punch2_out': ['punch2 out', 'punch2_out', 'out', 'out_time'],
                        'punch3_in': ['punch3 in', 'punch3_in', 'in (2)', 'in_time_2'],
                        'punch4_out': ['punch4 out', 'punch4_out', 'out (2)', 'out_time_2'],
                        'punch5_in': ['punch5 in', 'punch5_in', 'in (3)', 'in_time_3'],
                        'punch6_out': ['punch6 out', 'punch6_out', 'out (3)', 'out_time_3'],
                        'overstay': ['overstay'],
                        'overtime': ['overtime'],
                        'regular_hours': ['regular_hours', 'regular hours', 'overtime_to_mandays', 'overtime to mandays'],
                        'hours_worked': ['hours_worked', 'hours worked', 'hours', 'hrs'],
                    }
                    
                    # Map to AttendanceRecord fields
                    attendance_field_mapping = {
                        'punch1_in': 'in_time',
                        'punch2_out': 'out_time',
                        'punch3_in': 'in_time_2',
                        'punch4_out': 'out_time_2',
                        'punch5_in': 'in_time_3',
                        'punch6_out': 'out_time_3',
                        'overtime': 'overtime',
                        'regular_hours': 'overtime_to_mandays',
                    }
                    
                    for source_field, possible_cols in time_field_mappings.items():
                        col = self._find_column(df, possible_cols)
                        if col and pd.notna(row.get(col)):
                            if source_field == 'overstay':
                                # Overstay is a CharField, format as HH:MM (not HH:MM:SS)
                                overstay_value = self._format_time_as_hhmm(row.get(col))
                                record_data['overstay'] = overstay_value if overstay_value else ''
                            elif source_field == 'hours_worked':
                                # Hours worked - store as string in HH:MM format
                                hours_value = self._format_time_as_hhmm(row.get(col))
                                record_data['hours'] = hours_value if hours_value else ''
                            elif source_field == 'regular_hours':
                                # Regular hours - store as string
                                regular_value = self._format_time_as_hhmm(row.get(col))
                                record_data['overtime_to_mandays'] = regular_value if regular_value else ''
                            else:
                                time_value = self._parse_time(row.get(col))
                                
                                # Map to AttendanceRecord field
                                if source_field in attendance_field_mapping:
                                    record_data[attendance_field_mapping[source_field]] = time_value
                    
                    # Check if record already exists
                    if AttendanceRecord.objects.filter(ep_no=str(ep_no), date=punchdate).exists():
                        duplicates += 1
                        # Update existing record
                        AttendanceRecord.objects.filter(ep_no=str(ep_no), date=punchdate).update(**record_data)
                    else:
                        # Create new record
                        AttendanceRecord.objects.create(
                            ep_no=str(ep_no),
                            date=punchdate,
                            **record_data
                        )
                        imported += 1
                    
                except Exception as e:
                    logger.error(f"Error importing record for EP {ep_no} on {punchdate}: {e}")
        
        logger.info(f"Imported {imported} attendance records, updated {duplicates} duplicates")
        return imported, duplicates
    
    def _format_time_as_hhmm(self, time_value):
        """
        Format time value as HH:MM string (without seconds)
        
        Args:
            time_value: Time string or value to format
            
        Returns:
            String in HH:MM format or None
        """
        if pd.isna(time_value):
            return None
        
        time_str = str(time_value).strip()
        
        # Handle "0" as no time
        if time_str in ['0', '0.0', '']:
            return None
        
        # Remove (N) indicator if present
        if '(' in time_str and ')' in time_str:
            time_str = time_str.split('(')[0].strip()
        
        # Parse time manually
        parts = time_str.split(':')
        if len(parts) < 2:
            return None
        
        try:
            hours = int(parts[0])
            minutes = int(parts[1])
            
            # Validate minutes
            if minutes < 0 or minutes > 59:
                return None
            
            # Normalize hours > 23 using modulo 24
            if hours >= 24:
                hours = hours % 24
            elif hours < 0:
                return None
            
            # Return formatted as HH:MM
            return f"{hours:02d}:{minutes:02d}"
        except (ValueError, TypeError):
            return None
    
    def _parse_time(self, time_value):
        """
        Parse time value with support for (N) indicator and hours > 24
        
        Args:
            time_value: Time string or value to parse
            
        Returns:
            time object or None
        """
        if pd.isna(time_value):
            return None
        
        time_str = str(time_value).strip()
        
        # Handle "0" as no time
        if time_str in ['0', '0.0', '']:
            return None
        
        # Remove (N) indicator if present
        if '(' in time_str and ')' in time_str:
            time_str = time_str.split('(')[0].strip()
        
        # Parse time manually to support hours > 24
        parts = time_str.split(':')
        if len(parts) < 2:
            return None
        
        try:
            from datetime import time as dt_time
            
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2]) if len(parts) >= 3 else 0
            
            # Validate minutes and seconds
            if minutes < 0 or minutes > 59 or seconds < 0 or seconds > 59:
                return None
            
            # Normalize hours > 23 using modulo 24
            if hours >= 24:
                hours = hours % 24
            elif hours < 0:
                return None
            
            return dt_time(hours, minutes, seconds)
        except (ValueError, TypeError):
            return None
    
    def create_or_update_contractors(self, df: pd.DataFrame) -> int:
        """
        Upsert contractor records
        
        Args:
            df: DataFrame containing contractor data
            
        Returns:
            Number of contractors created/updated
        """
        contractor_col = self._find_column(df, ['contractor_code', 'contractor code', 'contcode', 'cont_code'])
        name_col = self._find_column(df, ['contractor_name', 'contractor name'])
        
        if not contractor_col:
            return 0
        
        # Get unique contractors
        contractors_data = df[[contractor_col, name_col]].drop_duplicates() if name_col else df[[contractor_col]].drop_duplicates()
        
        count = 0
        for _, row in contractors_data.iterrows():
            code = row[contractor_col]
            name = row[name_col] if name_col else f"Contractor {code}"
            
            if pd.notna(code):
                Contractor.objects.update_or_create(
                    contractor_code=int(code),
                    defaults={'contractor_name': str(name)}
                )
                count += 1
        
        logger.info(f"Created/updated {count} contractors")
        return count
    
    def create_or_update_employees(self, df: pd.DataFrame) -> int:
        """
        Upsert employee records
        
        Args:
            df: DataFrame containing employee data
            
        Returns:
            Number of employees created/updated
        """
        ep_col = self._find_column(df, ['ep_no', 'ep no', 'epno'])
        name_col = self._find_column(df, ['ep_name', 'ep name', 'epname', 'employee_name'])
        contractor_col = self._find_column(df, ['contractor_code', 'contractor code', 'contcode'])
        
        if not ep_col or not contractor_col:
            return 0
        
        # Get unique employees
        required_cols = [ep_col, contractor_col]
        if name_col:
            required_cols.append(name_col)
        
        employees_data = df[required_cols].drop_duplicates(subset=[ep_col])
        
        count = 0
        for _, row in employees_data.iterrows():
            ep_no = row[ep_col]
            contractor_code = row[contractor_col]
            ep_name = row[name_col] if name_col else f"Employee {ep_no}"
            
            if pd.notna(ep_no) and pd.notna(contractor_code):
                try:
                    contractor = Contractor.objects.get(contractor_code=int(contractor_code))
                    
                    Employee.objects.update_or_create(
                        ep_no=str(ep_no),
                        defaults={
                            'ep_name': str(ep_name),
                            'contractor': contractor
                        }
                    )
                    count += 1
                except Contractor.DoesNotExist:
                    logger.warning(f"Contractor {contractor_code} not found for employee {ep_no}")
        
        logger.info(f"Created/updated {count} employees")
        return count
    
    def import_punch_records(self, df: pd.DataFrame) -> Tuple[int, int]:
        """
        Import punch records with duplicate skipping
        
        Args:
            df: DataFrame containing punch records
            
        Returns:
            Tuple of (imported_count, duplicate_count)
        """
        ep_col = self._find_column(df, ['ep_no', 'ep no'])
        date_col = self._find_column(df, ['punchdate', 'punch_date'])
        
        if not ep_col or not date_col:
            return 0, 0
        
        imported = 0
        duplicates = 0
        
        for _, row in df.iterrows():
            ep_no = row[ep_col]
            punchdate = row[date_col]
            
            if pd.notna(ep_no) and pd.notna(punchdate):
                try:
                    employee = Employee.objects.get(ep_no=str(ep_no))
                    
                    # Check if record already exists
                    if PunchRecord.objects.filter(employee=employee, punchdate=punchdate).exists():
                        duplicates += 1
                        continue
                    
                    # Create new record
                    PunchRecord.objects.create(
                        employee=employee,
                        punchdate=punchdate,
                        shift=row.get('shift', ''),
                        punch1_in=row.get('punch1_in'),
                        punch2_out=row.get('punch2_out'),
                        punch3_in=row.get('punch3_in'),
                        punch4_out=row.get('punch4_out'),
                        punch5_in=row.get('punch5_in'),
                        punch6_out=row.get('punch6_out'),
                        hours_worked=row.get('hours_worked'),
                        overstay=row.get('overstay'),
                        status=row.get('status', 'P')
                    )
                    imported += 1
                    
                except Employee.DoesNotExist:
                    logger.warning(f"Employee {ep_no} not found")
        
        logger.info(f"Imported {imported} punch records, skipped {duplicates} duplicates")
        return imported, duplicates
    
    def import_daily_summaries(self, df: pd.DataFrame) -> Tuple[int, int]:
        """
        Import daily summary records
        
        Args:
            df: DataFrame containing daily summaries
            
        Returns:
            Tuple of (imported_count, duplicate_count)
        """
        ep_col = self._find_column(df, ['ep_no', 'epno'])
        date_col = self._find_column(df, ['punchdate', 'punch_date'])
        
        if not ep_col or not date_col:
            return 0, 0
        
        imported = 0
        duplicates = 0
        
        for _, row in df.iterrows():
            ep_no = row[ep_col]
            punchdate = row[date_col]
            
            if pd.notna(ep_no) and pd.notna(punchdate):
                try:
                    employee = Employee.objects.get(ep_no=str(ep_no))
                    
                    # Check if record already exists
                    if DailySummary.objects.filter(employee=employee, punchdate=punchdate).exists():
                        duplicates += 1
                        continue
                    
                    # Create new record
                    DailySummary.objects.create(
                        employee=employee,
                        punchdate=punchdate,
                        mandays=row.get('mandays', 0),
                        regular_manday_hr=row.get('regular_manday_hr'),
                        ot=row.get('ot', 0),
                        location_status=row.get('location_status', '')
                    )
                    imported += 1
                    
                except Employee.DoesNotExist:
                    logger.warning(f"Employee {ep_no} not found")
        
        logger.info(f"Imported {imported} daily summaries, skipped {duplicates} duplicates")
        return imported, duplicates
    
    def import_overtime_requests(self, df: pd.DataFrame) -> Tuple[int, int]:
        """
        Import overtime request records
        
        Args:
            df: DataFrame containing overtime requests
            
        Returns:
            Tuple of (imported_count, duplicate_count)
        """
        ep_col = self._find_column(df, ['ep_no', 'ep no'])
        date_col = self._find_column(df, ['punchdate', 'punch_date'])
        
        if not ep_col or not date_col:
            return 0, 0
        
        imported = 0
        duplicates = 0
        
        for _, row in df.iterrows():
            ep_no = row[ep_col]
            punchdate = row[date_col]
            
            if pd.notna(ep_no) and pd.notna(punchdate):
                try:
                    employee = Employee.objects.get(ep_no=str(ep_no))
                    
                    # Check if record already exists
                    if OvertimeRequest.objects.filter(employee=employee, punchdate=punchdate).exists():
                        duplicates += 1
                        continue
                    
                    # Create new record
                    OvertimeRequest.objects.create(
                        employee=employee,
                        punchdate=punchdate,
                        actual_overstay=row.get('actual_overstay'),
                        requested_overtime=row.get('requested_overtime'),
                        approved_overtime=row.get('approved_overtime'),
                        status=row.get('ot_request_status', 'Pending')
                    )
                    imported += 1
                    
                except Employee.DoesNotExist:
                    logger.warning(f"Employee {ep_no} not found")
        
        logger.info(f"Imported {imported} overtime requests, skipped {duplicates} duplicates")
        return imported, duplicates
    
    def import_partial_day_requests(self, df: pd.DataFrame) -> Tuple[int, int]:
        """
        Import partial day request records
        
        Args:
            df: DataFrame containing partial day requests
            
        Returns:
            Tuple of (imported_count, duplicate_count)
        """
        ep_col = self._find_column(df, ['ep_no', 'ep no'])
        date_col = self._find_column(df, ['punchdate', 'punch_date'])
        
        if not ep_col or not date_col:
            return 0, 0
        
        imported = 0
        duplicates = 0
        
        for _, row in df.iterrows():
            ep_no = row[ep_col]
            punchdate = row[date_col]
            
            if pd.notna(ep_no) and pd.notna(punchdate):
                try:
                    employee = Employee.objects.get(ep_no=str(ep_no))
                    
                    # Check if record already exists
                    if PartialDayRequest.objects.filter(employee=employee, punchdate=punchdate).exists():
                        duplicates += 1
                        continue
                    
                    # Create new record
                    PartialDayRequest.objects.create(
                        employee=employee,
                        punchdate=punchdate,
                        actual_pd_hours=row.get('actual_pd_hours'),
                        requested_pd_hours=row.get('requested_pd_hours'),
                        approved_pd_hours=row.get('approved_pd_hours'),
                        manday_conversion=row.get('manday_conversion', 0),
                        status=row.get('pd_request_status', 'Pending')
                    )
                    imported += 1
                    
                except Employee.DoesNotExist:
                    logger.warning(f"Employee {ep_no} not found")
        
        logger.info(f"Imported {imported} partial day requests, skipped {duplicates} duplicates")
        return imported, duplicates
    
    def import_regularization_requests(self, df: pd.DataFrame) -> Tuple[int, int]:
        """
        Import regularization request records
        
        Args:
            df: DataFrame containing regularization requests
            
        Returns:
            Tuple of (imported_count, duplicate_count)
        """
        ep_col = self._find_column(df, ['ep_no', 'ep no'])
        date_col = self._find_column(df, ['punchdate', 'punch_date'])
        
        if not ep_col or not date_col:
            return 0, 0
        
        imported = 0
        duplicates = 0
        
        for _, row in df.iterrows():
            ep_no = row[ep_col]
            punchdate = row[date_col]
            
            if pd.notna(ep_no) and pd.notna(punchdate):
                try:
                    employee = Employee.objects.get(ep_no=str(ep_no))
                    
                    # Check if record already exists
                    if RegularizationRequest.objects.filter(employee=employee, punchdate=punchdate).exists():
                        duplicates += 1
                        continue
                    
                    # Create new record
                    RegularizationRequest.objects.create(
                        employee=employee,
                        punchdate=punchdate,
                        old_punch_in=row.get('old_punch_in'),
                        old_punch_out=row.get('old_punch_out'),
                        new_punch_in=row.get('new_punch_in'),
                        new_punch_out=row.get('new_punch_out'),
                        status=row.get('request_status', 'Pending')
                    )
                    imported += 1
                    
                except Employee.DoesNotExist:
                    logger.warning(f"Employee {ep_no} not found")
        
        logger.info(f"Imported {imported} regularization requests, skipped {duplicates} duplicates")
        return imported, duplicates
    
    def _find_column(self, df: pd.DataFrame, possible_names: List[str]) -> str:
        """
        Find column by possible names (case-insensitive)
        
        Args:
            df: DataFrame to search
            possible_names: List of possible column names
            
        Returns:
            Actual column name or None
        """
        columns_lower = {col.lower(): col for col in df.columns}
        
        for name in possible_names:
            name_lower = name.lower()
            if name_lower in columns_lower:
                return columns_lower[name_lower]
        
        return None
