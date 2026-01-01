"""Data Validator Service for Excel File Upload Integration"""
import re
import pandas as pd
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    is_valid: bool
    error_message: str = ""

@dataclass
class ValidationError:
    row_number: int
    column_name: str
    value: str
    error_message: str

@dataclass
class ValidationReport:
    total_rows: int
    valid_rows: int
    invalid_rows: int
    errors: List[ValidationError]
    duplicates: List[int]
    
    def to_dict(self) -> Dict:
        return {
            'total_rows': self.total_rows,
            'valid_rows': self.valid_rows,
            'invalid_rows': self.invalid_rows,
            'error_count': len(self.errors),
            'duplicate_count': len(self.duplicates),
            'errors': [{'row': e.row_number, 'column': e.column_name, 'value': e.value, 'message': e.error_message} for e in self.errors],
            'duplicates': self.duplicates
        }

class DataValidatorService:
    """Service for validating uploaded data - supports hours > 24"""
    
    def __init__(self):
        # Patterns defined in __init__ to avoid regex escaping issues
        self.EP_NO_PATTERN = re.compile(r'^(PP|VP)\d{10}' + r'$')
        # Allow 1-3 digits for hours (supports 25:30, 48:00, 100:00)
        self.TIME_PATTERN = re.compile(r'^\d{1,3}:\d{2}(:\d{2})?(\s*\([A-Z]\))?' + r'$')


    def validate_ep_no(self, ep_no):
        if not ep_no or pd.isna(ep_no):
            return ValidationResult(False, "EP NO is required")
        ep_no_str = str(ep_no).strip()
        if not self.EP_NO_PATTERN.match(ep_no_str):
            return ValidationResult(False, f"Invalid EP NO: {ep_no_str}")
        return ValidationResult(True)

    def validate_date(self, date_str):
        if not date_str or pd.isna(date_str):
            return ValidationResult(False, "Date is required")
        date_str = str(date_str).strip()
        for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']:
            try:
                parsed = datetime.strptime(date_str, fmt)
                if parsed.date() > datetime.now().date():
                    return ValidationResult(False, f"Future date: {date_str}")
                return ValidationResult(True)
            except ValueError:
                continue
        return ValidationResult(False, f"Invalid date: {date_str}")

    def validate_time(self, time_str):
        """Validate time - supports HH:MM, HH:MM:SS, with (N), hours > 24"""
        if not time_str or pd.isna(time_str) or str(time_str).strip() == '':
            return ValidationResult(True)
        time_str = str(time_str).strip()
        if time_str in ('0', '0.0'):
            return ValidationResult(True)
        if not self.TIME_PATTERN.match(time_str):
            return ValidationResult(False, f"Invalid time: {time_str}")
        clean = time_str.split('(')[0].strip() if '(' in time_str else time_str
        parts = clean.split(':')
        try:
            hours = int(parts[0])
            minutes = int(parts[1])
            if hours < 0 or minutes < 0 or minutes > 59:
                return ValidationResult(False, f"Invalid time: {time_str}")
            if len(parts) == 3:
                seconds = int(parts[2])
                if seconds < 0 or seconds > 59:
                    return ValidationResult(False, f"Invalid seconds: {time_str}")
        except ValueError:
            return ValidationResult(False, f"Invalid time: {time_str}")
        return ValidationResult(True)

    def validate_foreign_keys(self, df):
        from core.models import Contractor
        errors = []
        contractor_col = None
        for col in df.columns:
            if 'contractor' in col.lower() and 'code' in col.lower():
                contractor_col = col
                break
        if contractor_col and contractor_col in df.columns:
            existing = set(Contractor.objects.values_list('contractor_code', flat=True))
            for idx, row in df.iterrows():
                code = row[contractor_col]
                if pd.notna(code) and int(code) not in existing:
                    errors.append(ValidationError(idx + 2, contractor_col, str(code), f"Contractor {code} not found"))
        return errors

    def validate_batch(self, df, file_type):
        if df is None or df.empty:
            return ValidationReport(0, 0, 0, [], [])
        errors = []
        total = len(df)
        ep_col = self._find_column(df, ['ep_no', 'ep no', 'epno'])
        if ep_col:
            for idx, val in df[ep_col].items():
                r = self.validate_ep_no(val)
                if not r.is_valid:
                    errors.append(ValidationError(idx + 2, ep_col, str(val), r.error_message))
        date_col = self._find_column(df, ['punchdate', 'punch_date', 'date'])
        if date_col:
            for idx, val in df[date_col].items():
                r = self.validate_date(val)
                if not r.is_valid:
                    errors.append(ValidationError(idx + 2, date_col, str(val), r.error_message))
        time_cols = [c for c in df.columns if any(k in c.lower() for k in ['time', 'hours', 'in', 'out', 'overstay', 'overtime'])]
        for tc in time_cols:
            for idx, val in df[tc].items():
                r = self.validate_time(val)
                if not r.is_valid:
                    errors.append(ValidationError(idx + 2, tc, str(val), r.error_message))
        errors.extend(self.validate_foreign_keys(df))
        dups = self.detect_duplicates(df)
        invalid = len(set(e.row_number for e in errors))
        return ValidationReport(total, total - invalid, invalid, errors, dups)

    def detect_duplicates(self, df):
        from core.models import PunchRecord, DailySummary, OvertimeRequest, PartialDayRequest, RegularizationRequest
        dups = []
        ep_col = self._find_column(df, ['ep_no', 'ep no', 'epno'])
        date_col = self._find_column(df, ['punchdate', 'punch_date', 'date'])
        if not ep_col or not date_col:
            return dups
        df_dups = df[df.duplicated(subset=[ep_col, date_col], keep=False)]
        if not df_dups.empty:
            dups.extend(df_dups.index.tolist())
        for idx, row in df.iterrows():
            ep, dt = row[ep_col], row[date_col]
            if pd.notna(ep) and pd.notna(dt):
                exists = (
                    PunchRecord.objects.filter(employee__ep_no=ep, punchdate=dt).exists() or
                    DailySummary.objects.filter(employee__ep_no=ep, punchdate=dt).exists() or
                    OvertimeRequest.objects.filter(employee__ep_no=ep, punchdate=dt).exists() or
                    PartialDayRequest.objects.filter(employee__ep_no=ep, punchdate=dt).exists() or
                    RegularizationRequest.objects.filter(employee__ep_no=ep, punchdate=dt).exists()
                )
                if exists and idx not in dups:
                    dups.append(idx)
        return dups

    def _find_column(self, df, names):
        cols = {c.lower(): c for c in df.columns}
        for n in names:
            if n.lower() in cols:
                return cols[n.lower()]
        return None
