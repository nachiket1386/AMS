#!/usr/bin/env python
"""Check OT values after migration"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import MandaySummaryRecord

# Get sample records
records = MandaySummaryRecord.objects.all()[:10]

print("Sample OT values after migration:")
print("-" * 60)
for r in records:
    print(f"{r.ep_no:15s} | OT: {r.ot:8} | Type: {type(r.ot).__name__}")
print("-" * 60)
print(f"Total records: {MandaySummaryRecord.objects.count()}")
