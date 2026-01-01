#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import MandaySummaryRecord

records = MandaySummaryRecord.objects.all()[:5]
print("Current date display format:")
for record in records:
    print(f"  {record.ep_no}: {record.punch_date.strftime('%d-%m-%Y')}")
