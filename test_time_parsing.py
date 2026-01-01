#!/usr/bin/env python
"""
Quick test script to verify time format parsing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.manday_processor import MandayProcessor
from core.models import User, Company
from datetime import time

# Create test processor
processor = MandayProcessor()

# Test time format parsing
test_cases = [
    ('08:30', time(8, 30)),
    ('09:00', time(9, 0)),
    ('04:15', time(4, 15)),
    ('00:00', time(0, 0)),
    ('23:59', time(23, 59)),
    ('8.5', time(8, 30)),  # Decimal format
    ('9.0', time(9, 0)),
    ('4.25', time(4, 15)),
]

print("Testing time format parsing...")
print("-" * 50)

for input_val, expected_time in test_cases:
    # Parse to decimal
    decimal_val = processor.validate_time_to_decimal(input_val, 'test')
    
    # Convert to time
    time_val = processor.decimal_hours_to_time(decimal_val)
    
    status = "✓" if time_val == expected_time else "✗"
    print(f"{status} Input: {input_val:10s} -> Decimal: {decimal_val:6.2f} -> Time: {time_val} (Expected: {expected_time})")

print("-" * 50)
print("Testing complete!")
