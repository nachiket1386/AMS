"""Verify that all models were created successfully"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import (
    Employee, Contractor, Plant,
    PunchRecord, DailySummary, OvertimeRequest, PartialDayRequest, RegularizationRequest,
    ImportLog, ExportLog, UploadPermission
)

print("✓ All models imported successfully!")
print("\nMaster Tables:")
print(f"  - Employee: {Employee._meta.db_table}")
print(f"  - Contractor: {Contractor._meta.db_table}")
print(f"  - Plant: {Plant._meta.db_table}")

print("\nTransaction Tables:")
print(f"  - PunchRecord: {PunchRecord._meta.db_table}")
print(f"  - DailySummary: {DailySummary._meta.db_table}")
print(f"  - OvertimeRequest: {OvertimeRequest._meta.db_table}")
print(f"  - PartialDayRequest: {PartialDayRequest._meta.db_table}")
print(f"  - RegularizationRequest: {RegularizationRequest._meta.db_table}")

print("\nAudit Tables:")
print(f"  - ImportLog: {ImportLog._meta.db_table}")
print(f"  - ExportLog: {ExportLog._meta.db_table}")
print(f"  - UploadPermission: {UploadPermission._meta.db_table}")

print("\n✓ Schema verification complete!")
