"""
BackupService for creating database backups
"""
import json
import hashlib
from datetime import datetime
from django.utils import timezone
from core.models import Company, AttendanceRecord


class BackupService:
    """Service for creating full and incremental backups"""
    
    def create_backup(self, backup_type='full', since_date=None):
        """
        Create a backup of attendance data
        
        Args:
            backup_type: 'full' or 'incremental'
            since_date: For incremental backups, only include records modified after this date
            
        Returns:
            dict with keys: 'success', 'data', 'record_count', 'metadata'
        """
        try:
            # Query companies
            companies = Company.objects.all()
            
            # Query attendance records
            if backup_type == 'incremental' and since_date:
                attendance_records = AttendanceRecord.objects.filter(
                    updated_at__gte=since_date
                )
            else:
                attendance_records = AttendanceRecord.objects.all()
            
            # Serialize data
            companies_data = [self._serialize_company(c) for c in companies]
            attendance_data = [self._serialize_record(r) for r in attendance_records.select_related('company')]
            
            # Create metadata
            metadata = self._create_metadata(
                backup_type=backup_type,
                companies_count=len(companies_data),
                records_count=len(attendance_data),
                since_date=since_date
            )
            
            # Build backup structure
            backup_data = {
                'metadata': metadata,
                'companies': companies_data,
                'attendance_records': attendance_data
            }
            
            return {
                'success': True,
                'data': backup_data,
                'companies_count': len(companies_data),
                'records_count': len(attendance_data),
                'metadata': metadata
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'data': None
            }
    
    def create_incremental_backup(self, since_date):
        """
        Create an incremental backup with records modified after since_date
        
        Args:
            since_date: Only include records with updated_at >= since_date
            
        Returns:
            dict with keys: 'success', 'data', 'record_count', 'metadata'
        """
        return self.create_backup(backup_type='incremental', since_date=since_date)
    
    def _serialize_company(self, company):
        """Convert Company model instance to dict"""
        data = {
            'id': company.id,
            'name': company.name,
            'created_at': company.created_at.isoformat() if company.created_at else None,
        }
        data['checksum'] = self._generate_checksum(data)
        return data
    
    def _serialize_record(self, record):
        """Convert AttendanceRecord model instance to dict"""
        data = {
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
            'created_at': record.created_at.isoformat() if record.created_at else None,
            'updated_at': record.updated_at.isoformat() if record.updated_at else None,
        }
        data['checksum'] = self._generate_checksum(data)
        return data
    
    def _generate_checksum(self, record):
        """Generate SHA256 checksum for a record"""
        # Create a copy without checksum field and timestamps (for consistency)
        exclude_fields = {'checksum', 'created_at', 'updated_at', 'id'}
        data_copy = {k: v for k, v in record.items() if k not in exclude_fields}
        
        # Sort keys for consistent hashing
        sorted_data = json.dumps(data_copy, sort_keys=True, default=str)
        
        # Generate SHA256 hash
        return hashlib.sha256(sorted_data.encode('utf-8')).hexdigest()
    
    def _create_metadata(self, backup_type, companies_count, records_count, since_date=None):
        """Create backup metadata"""
        metadata = {
            'version': '1.0',
            'created_at': timezone.now().isoformat(),
            'backup_type': backup_type,
            'total_companies': companies_count,
            'total_attendance_records': records_count,
        }
        
        if since_date:
            metadata['since_date'] = since_date.isoformat() if hasattr(since_date, 'isoformat') else str(since_date)
        
        return metadata
