"""
Export Service for Excel File Upload Integration

This service handles exporting data to various formats (CSV, Excel).
"""
import pandas as pd
from datetime import datetime
from typing import Iterator
import logging

from core.models import ExportLog, User

logger = logging.getLogger(__name__)


class ExportService:
    """Service for exporting data to files"""
    
    def export_to_csv(self, queryset, filename: str = None) -> str:
        """
        Export queryset to CSV file
        
        Args:
            queryset: Django QuerySet to export
            filename: Optional filename (auto-generated if not provided)
            
        Returns:
            Path to generated CSV file
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"export_{timestamp}.csv"
        
        # Convert queryset to DataFrame
        data = list(queryset.values())
        df = pd.DataFrame(data)
        
        # Generate CSV
        csv_path = f"/tmp/{filename}"
        df.to_csv(csv_path, index=False)
        
        logger.info(f"Exported {len(df)} records to {csv_path}")
        return csv_path
    
    def export_to_excel(self, queryset, filename: str = None) -> str:
        """
        Export queryset to Excel file
        
        Args:
            queryset: Django QuerySet to export
            filename: Optional filename (auto-generated if not provided)
            
        Returns:
            Path to generated Excel file
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"export_{timestamp}.xlsx"
        
        # Convert queryset to DataFrame
        data = list(queryset.values())
        df = pd.DataFrame(data)
        
        # Generate Excel
        excel_path = f"/tmp/{filename}"
        df.to_excel(excel_path, index=False, engine='openpyxl')
        
        logger.info(f"Exported {len(df)} records to {excel_path}")
        return excel_path
    
    def stream_export(self, queryset, format: str = 'csv') -> Iterator:
        """
        Stream large exports to avoid memory issues
        
        Args:
            queryset: Django QuerySet to export
            format: Export format ('csv' or 'excel')
            
        Yields:
            Chunks of export data
        """
        batch_size = 1000
        
        # Get column names from first record
        first_record = queryset.first()
        if not first_record:
            return
        
        columns = list(first_record.__dict__.keys())
        columns = [col for col in columns if not col.startswith('_')]
        
        # Yield header
        if format == 'csv':
            yield ','.join(columns) + '\n'
        
        # Yield data in batches
        offset = 0
        while True:
            batch = queryset[offset:offset + batch_size]
            if not batch:
                break
            
            for record in batch:
                values = [str(getattr(record, col, '')) for col in columns]
                if format == 'csv':
                    yield ','.join(values) + '\n'
            
            offset += batch_size
    
    def generate_filename(self, export_type: str, user: User = None) -> str:
        """
        Generate filename with timestamp
        
        Args:
            export_type: Type of export (e.g., 'attendance', 'punch_records')
            user: Optional user for personalized filename
            
        Returns:
            Generated filename
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if user:
            return f"{export_type}_{user.username}_{timestamp}.csv"
        else:
            return f"{export_type}_{timestamp}.csv"
    
    def log_export(self, user: User, export_type: str, record_count: int, filters: dict = None) -> ExportLog:
        """
        Create export log entry
        
        Args:
            user: User performing export
            export_type: Type of data exported
            record_count: Number of records exported
            filters: Filters applied to export
            
        Returns:
            ExportLog object
        """
        log = ExportLog.objects.create(
            user=user,
            export_type=export_type,
            record_count=record_count,
            filters=filters or {}
        )
        
        logger.info(f"Export logged: {export_type} - {record_count} records by {user.username}")
        return log
