"""
Management command to restore database from backup
"""
from django.core.management.base import BaseCommand
import json
import sys


class Command(BaseCommand):
    help = 'Restore attendance data from a backup file'
    
    def add_arguments(self, parser):
        parser.add_argument('--input', type=str, required=True, help='Input backup file path')
        parser.add_argument('--strategy', type=str, default='backup_wins', choices=['backup_wins', 'database_wins'], help='Merge strategy')
        parser.add_argument('--preview', action='store_true', help='Preview changes without applying')
    
    def handle(self, *args, **options):
        from core.services.restore_service import RestoreService
        
        input_path = options['input']
        merge_strategy = options['strategy']
        preview_only = options['preview']
        
        # Read backup file
        try:
            with open(input_path, 'r') as f:
                backup_data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {input_path}'))
            sys.exit(1)
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON file'))
            sys.exit(1)
        
        service = RestoreService()
        
        # Validate backup
        self.stdout.write('Validating backup...')
        validation = service.validate_backup(backup_data)
        
        if not validation['valid']:
            self.stdout.write(self.style.ERROR('Validation failed:'))
            for error in validation['errors']:
                self.stdout.write(f'  - {error}')
            sys.exit(1)
        
        self.stdout.write(self.style.SUCCESS('✓ Backup valid'))
        
        # Preview changes
        self.stdout.write('Analyzing changes...')
        preview = service.preview_changes(backup_data)
        
        self.stdout.write(f'\nPreview Summary:')
        self.stdout.write(f'  Records to add:    {preview["summary"]["add_count"]}')
        self.stdout.write(f'  Records to update: {preview["summary"]["update_count"]}')
        self.stdout.write(f'  Records to skip:   {preview["summary"]["skip_count"]}')
        self.stdout.write(f'  Conflicts:         {preview["summary"]["conflict_count"]}')
        
        if preview_only:
            self.stdout.write(self.style.SUCCESS('\n✓ Preview complete (no changes applied)'))
            sys.exit(0)
        
        # Apply restore
        self.stdout.write(f'\nApplying restore with strategy: {merge_strategy}')
        result = service.restore_backup(backup_data, merge_strategy=merge_strategy)
        
        if result['success']:
            self.stdout.write(self.style.SUCCESS('\n✓ Restore completed successfully'))
            self.stdout.write(f'  Added:   {result["added"]}')
            self.stdout.write(f'  Updated: {result["updated"]}')
            self.stdout.write(f'  Skipped: {result["skipped"]}')
            
            if result.get('errors'):
                self.stdout.write(self.style.WARNING(f'\nWarnings: {len(result["errors"])}'))
                for error in result['errors'][:5]:
                    self.stdout.write(f'  - {error}')
            
            sys.exit(0)
        else:
            self.stdout.write(self.style.ERROR('\n✗ Restore failed'))
            for error in result.get('errors', []):
                self.stdout.write(f'  - {error}')
            sys.exit(1)
