#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.manday_processor import MandayProcessor
from core.models import User, MandaySummaryRecord

# Get a user
user = User.objects.filter(role='admin').first() or User.objects.filter(role='root').first()
print(f'Testing with user: {user.username if user else "No user found"}')

if not user:
    print("ERROR: No admin or root user found!")
    exit(1)

# Create mock file
class MockFile:
    def __init__(self, filename):
        self.name = filename
        with open(filename, 'rb') as f:
            self.content = f.read()
        self.size = len(self.content)
    
    def read(self):
        return self.content
    
    def seek(self, position):
        pass

# Test upload
processor = MandayProcessor()
mock_file = MockFile('sample_mandays.csv')

print(f'\nProcessing file: {mock_file.name}')
print(f'File size: {mock_file.size} bytes')

result = processor.process_csv(mock_file, user)

print(f'\n=== RESULTS ===')
print(f'Success: {result["success_count"]}')
print(f'Updated: {result["updated_count"]}')
print(f'Errors: {result["error_count"]}')
print(f'Total rows: {result["total_rows"]}')

if result['errors']:
    print(f'\nErrors:')
    for error in result['errors'][:5]:
        print(f'  - {error}')

# Check database
count = MandaySummaryRecord.objects.count()
print(f'\nTotal records in database: {count}')

if count > 0:
    print('\nSample records:')
    for record in MandaySummaryRecord.objects.all()[:3]:
        print(f'  {record.ep_no} - {record.punch_date} - {record.mandays} mandays')
