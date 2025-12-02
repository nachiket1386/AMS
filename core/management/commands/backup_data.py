"""
Management command to create database backups
"""
from django.core.management.base import BaseCommand
from datetime import datetime
import json
import sys


class Command(BaseCommand):
    help = 'Create a backup of attendance data'
    
    def add_arguments(self, parser):
        parser.add_argument('--type', type=str, default='full', choices=['full', 'incremental'], help='Backup type')
        parser.add_argument('--output', type=str, help='Output file path')
        parser.add_argument('--since', type=str, help='For incremental: date (YYYY-MM-DD)')
    
    def handle(self, *args, **options):
        from core.services.backup_service import BackupService
        
        backup_type = options['type']
        output_path = options['output']
        since_date_str = options['since']
        
        since_date = None
        if backup_type == 'incremental':
            if since_date_str:
                try:
                    since_date = datetime.strptime(since_date_str, '%Y-%m-%d')
                except ValueError:
                    self.stdout.write(self.style.ERROR(f'Invalid date: {since_date_str}'))
                    sys.exit(1)
            else:
                self.stdout.write(self.style.ERROR('--since required for incremental'))
                sys.exit(1)
        
        if not output_path:
            output_path = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        self.stdout.write(f'Creating {backup_type} backup...')
        
        service = BackupService()
        result = service.create_incremental_backup(since_date) if backup_type == 'incremental' and since_date else service.create_backup()
        
        if not result['success']:
            self.stdout.write(self.style.ERROR(f'Failed: {result.get("error")}'))
            sys.exit(1)
        
        try:
            with open(output_path, 'w') as f:
                json.dump(result['data'], f, indent=2)
            
            self.stdout.write(self.style.SUCCESS(f'✓ Backup created'))
            self.stdout.write(f'  File: {output_path}')
            self.stdout.write(f'  Companies: {result["companies_count"]}')
            self.stdout.write(f'  Records: {result["records_count"]}')
            sys.exit(0)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            sys.exit(1)
