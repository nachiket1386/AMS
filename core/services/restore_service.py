"""
RestoreService for restoring database backups
"""
import json
from datetime import datetime
from django.utils import timezone
from core.models import Company, AttendanceRecord
from core.services.conflict_resolver import ConflictResolver


class RestoreService:
    """Service for restoring data from backup files with intelligent merging"""
    
    def __init__(self, conflict_resolver=None):
        self.conflict_resolver = conflict_resolver or ConflictResolver()
    
    def validate_backup(self, backup_data):
        """
        Validate backup file structure and content
        
        Args:
            backup_data: Dict containing backup data
            
        Returns:
            dict with keys: 'valid', 'errors', 'warnings'
        """
        errors = []
        warnings = []
        
        try:
            # Check if backup_data is a dict
            if not isinstance(backup_data, dict):
                errors.append("Backup data must be a JSON object")
                return {'valid': False, 'errors': errors, 'warnings': warnings}
            
            # Check required top-level keys
            required_keys = ['metadata', 'companies', 'attendance_records']
            for key in required_keys:
                if key not in backup_data:
                    errors.append(f"Missing required field: {key}")
            
            if errors:
                return {'valid': False, 'errors': errors, 'warnings': warnings}
            
            # Validate metadata
            metadata = backup_data['metadata']
            required_metadata = ['version', 'created_at', 'backup_type', 'total_companies', 'total_attendance_records']
            for key in required_metadata:
                if key not in metadata:
                    errors.append(f"Missing required metadata field: {key}")
            
            # Validate companies structure
            companies = backup_data['companies']
            if not isinstance(companies, list):
                errors.append("Companies must be a list")
            else:
                for i, company in enumerate(companies):
                    if not isinstance(company, dict):
                        errors.append(f"Company at index {i} must be an object")
                        continue
                    if 'name' not in company:
                        errors.append(f"Company at index {i} missing required field: name")
            
            # Validate attendance records structure
            records = backup_data['attendance_records']
            if not isinstance(records, list):
                errors.append("Attendance records must be a list")
            else:
                required_record_fields = ['ep_no', 'ep_name', 'company_name', 'date', 'status']
                for i, record in enumerate(records[:10]):  # Check first 10 records
                    if not isinstance(record, dict):
                        errors.append(f"Record at index {i} must be an object")
                        continue
                    for field in required_record_fields:
                        if field not in record:
                            errors.append(f"Record at index {i} missing required field: {field}")
                            break
            
            # Check counts match
            if len(companies) != metadata.get('total_companies', 0):
                warnings.append(f"Company count mismatch: metadata says {metadata.get('total_companies')}, found {len(companies)}")
            
            if len(records) != metadata.get('total_attendance_records', 0):
                warnings.append(f"Record count mismatch: metadata says {metadata.get('total_attendance_records')}, found {len(records)}")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings
            }
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return {'valid': False, 'errors': errors, 'warnings': warnings}
    
    def preview_changes(self, backup_data):
        """
        Analyze what changes would be made without applying them
        
        Args:
            backup_data: Dict containing backup data
            
        Returns:
            dict with keys: 'to_add', 'to_update', 'to_skip', 'conflicts'
        """
        to_add = []
        to_update = []
        to_skip = []
        conflicts = []
        
        try:
            # Get existing records from database
            existing_records = {}
            for record in AttendanceRecord.objects.all().select_related('company'):
                key = self._get_unique_key_from_model(record)
                existing_records[key] = record
            
            # Analyze each backup record
            for backup_record in backup_data.get('attendance_records', []):
                key = self._get_unique_key(backup_record)
                
                if key not in existing_records:
                    # New record
                    to_add.append(backup_record)
                else:
                    # Existing record - check if it differs
                    db_record = existing_records[key]
                    db_record_dict = self._model_to_dict(db_record)
                    
                    if self.conflict_resolver.detect_conflicts(backup_record, db_record_dict):
                        # Record differs - needs update
                        to_update.append(backup_record)
                        conflicts.append({
                            'key': key,
                            'backup': backup_record,
                            'database': db_record_dict
                        })
                    else:
                        # Record is identical - skip
                        to_skip.append(backup_record)
            
            return {
                'to_add': to_add,
                'to_update': to_update,
                'to_skip': to_skip,
                'conflicts': conflicts,
                'summary': {
                    'add_count': len(to_add),
                    'update_count': len(to_update),
                    'skip_count': len(to_skip),
                    'conflict_count': len(conflicts)
                }
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'to_add': [],
                'to_update': [],
                'to_skip': [],
                'conflicts': []
            }
    
    def _get_unique_key(self, record):
        """Generate unique key for record matching (ep_no, company_name, date)"""
        return (
            record.get('ep_no', ''),
            record.get('company_name', ''),
            record.get('date', '')
        )
    
    def _get_unique_key_from_model(self, record):
        """Generate unique key from Django model instance"""
        return (
            record.ep_no,
            record.company.name if record.company else '',
            record.date.isoformat() if record.date else ''
        )
    
    def _model_to_dict(self, record):
        """Convert Django model instance to dict for comparison"""
        return {
            'ep_no': record.ep_no,
            'ep_name': record.ep_name,
            'company_name': record.company.name if record.company else '',
            'date': record.date.isoformat() if record.date else None,
            'shift': record.shift or '',
            'overstay': record.overstay or '',
            'status': record.status,
            'in_time': record.in_time.strftime('%H:%M') if record.in_time else None,
            'out_time': record.out_time.strftime('%H:%M') if record.out_time else None,
            'in_time_2': record.in_time_2.strftime('%H:%M') if record.in_time_2 else None,
            'out_time_2': record.out_time_2.strftime('%H:%M') if record.out_time_2 else None,
            'in_time_3': record.in_time_3.strftime('%H:%M') if record.in_time_3 else None,
            'out_time_3': record.out_time_3.strftime('%H:%M') if record.out_time_3 else None,
            'overtime': record.overtime.strftime('%H:%M') if record.overtime else None,
            'overtime_to_mandays': record.overtime_to_mandays.strftime('%H:%M') if record.overtime_to_mandays else None,
        }
    
    def restore_backup(self, backup_data, merge_strategy='backup_wins', progress_callback=None):
        """
        Restore data from backup file with intelligent merging
        
        Args:
            backup_data: Dict containing backup data
            merge_strategy: 'backup_wins', 'database_wins', or 'manual'
            progress_callback: Optional function to call with progress updates
            
        Returns:
            dict with keys: 'success', 'added', 'updated', 'skipped', 'errors'
        """
        from django.db import transaction
        from datetime import datetime as dt
        
        added_count = 0
        updated_count = 0
        skipped_count = 0
        errors = []
        
        try:
            # Validate backup first
            validation = self.validate_backup(backup_data)
            if not validation['valid']:
                return {
                    'success': False,
                    'added': 0,
                    'updated': 0,
                    'skipped': 0,
                    'errors': validation['errors']
                }
            
            # Use transaction for atomicity
            with transaction.atomic():
                # Create company lookup cache
                company_cache = {}
                for company in Company.objects.all():
                    company_cache[company.name] = company
                
                # Get existing records
                existing_records = {}
                for record in AttendanceRecord.objects.all().select_related('company'):
                    key = self._get_unique_key_from_model(record)
                    existing_records[key] = record
                
                total_records = len(backup_data.get('attendance_records', []))
                
                # Process each backup record
                for idx, backup_record in enumerate(backup_data.get('attendance_records', [])):
                    try:
                        # Get or create company
                        company_name = backup_record.get('company_name', '')
                        if company_name not in company_cache:
                            company, created = Company.objects.get_or_create(name=company_name)
                            company_cache[company_name] = company
                        company = company_cache[company_name]
                        
                        # Get unique key
                        key = self._get_unique_key(backup_record)
                        
                        if key in existing_records:
                            # Record exists - check if it differs
                            db_record = existing_records[key]
                            db_record_dict = self._model_to_dict(db_record)
                            
                            if self.conflict_resolver.detect_conflicts(backup_record, db_record_dict):
                                # Conflict detected - apply merge strategy
                                merged_record = self.conflict_resolver.apply_merge_strategy(
                                    backup_record, db_record_dict, merge_strategy
                                )
                                
                                # Update the record
                                self._update_record_from_dict(db_record, merged_record)
                                db_record.save()
                                updated_count += 1
                            else:
                                # Records are identical - skip
                                skipped_count += 1
                        else:
                            # New record - create it
                            self._create_record_from_dict(backup_record, company)
                            added_count += 1
                        
                        # Progress callback
                        if progress_callback and (idx + 1) % 100 == 0:
                            progress_callback(idx + 1, total_records)
                    
                    except Exception as e:
                        errors.append(f"Error processing record {idx}: {str(e)}")
                
                # Final progress callback
                if progress_callback:
                    progress_callback(total_records, total_records)
            
            return {
                'success': True,
                'added': added_count,
                'updated': updated_count,
                'skipped': skipped_count,
                'errors': errors
            }
            
        except Exception as e:
            # Transaction will rollback automatically
            return {
                'success': False,
                'added': 0,
                'updated': 0,
                'skipped': 0,
                'errors': [f"Restore failed: {str(e)}"]
            }
    
    def _parse_time(self, time_str):
        """Parse time string to time object"""
        if not time_str:
            return None
        try:
            from datetime import datetime as dt
            return dt.strptime(time_str, '%H:%M').time()
        except:
            return None
    
    def _parse_date(self, date_str):
        """Parse date string to date object"""
        if not date_str:
            return None
        try:
            from datetime import datetime as dt
            return dt.fromisoformat(date_str).date()
        except:
            return None
    
    def _create_record_from_dict(self, record_dict, company):
        """Create new AttendanceRecord from dict"""
        AttendanceRecord.objects.create(
            ep_no=record_dict.get('ep_no', ''),
            ep_name=record_dict.get('ep_name', ''),
            company=company,
            date=self._parse_date(record_dict.get('date')),
            shift=record_dict.get('shift', ''),
            overstay=record_dict.get('overstay', ''),
            status=record_dict.get('status', 'P'),
            in_time=self._parse_time(record_dict.get('in_time')),
            out_time=self._parse_time(record_dict.get('out_time')),
            in_time_2=self._parse_time(record_dict.get('in_time_2')),
            out_time_2=self._parse_time(record_dict.get('out_time_2')),
            in_time_3=self._parse_time(record_dict.get('in_time_3')),
            out_time_3=self._parse_time(record_dict.get('out_time_3')),
            overtime=self._parse_time(record_dict.get('overtime')),
            overtime_to_mandays=self._parse_time(record_dict.get('overtime_to_mandays'))
        )
    
    def _update_record_from_dict(self, record, record_dict):
        """Update existing AttendanceRecord from dict"""
        record.ep_name = record_dict.get('ep_name', record.ep_name)
        record.shift = record_dict.get('shift', record.shift)
        record.overstay = record_dict.get('overstay', record.overstay)
        record.status = record_dict.get('status', record.status)
        record.in_time = self._parse_time(record_dict.get('in_time'))
        record.out_time = self._parse_time(record_dict.get('out_time'))
        record.in_time_2 = self._parse_time(record_dict.get('in_time_2'))
        record.out_time_2 = self._parse_time(record_dict.get('out_time_2'))
        record.in_time_3 = self._parse_time(record_dict.get('in_time_3'))
        record.out_time_3 = self._parse_time(record_dict.get('out_time_3'))
        record.overtime = self._parse_time(record_dict.get('overtime'))
        record.overtime_to_mandays = self._parse_time(record_dict.get('overtime_to_mandays'))
