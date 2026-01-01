"""
Property-based tests for MandayProcessor
Feature: mandays-overtime-summary
"""
from decimal import Decimal
from datetime import date, timedelta
from io import BytesIO, StringIO
from django.test import TestCase
from django.contrib.auth import get_user_model
from hypothesis import given, strategies as st, settings, assume
from hypothesis.extra.django import TestCase as HypothesisTestCase
from core.models import Company, MandaySummaryRecord
from core.manday_processor import MandayProcessor
import pandas as pd

User = get_user_model()


class MandayProcessorPropertyTests(HypothesisTestCase):
    """Property-based tests for MandayProcessor"""
    
    def setUp(self):
        """Set up test data"""
        self.company, _ = Company.objects.get_or_create(name="Test Processor Company")
        try:
            self.admin_user = User.objects.get(username='admin_processor')
        except User.DoesNotExist:
            self.admin_user = User.objects.create_user(
                username='admin_processor',
                password='testpass',
                role='admin',
                company=self.company
            )
        
        try:
            self.root_user = User.objects.get(username='root_processor')
        except User.DoesNotExist:
            self.root_user = User.objects.create_user(
                username='root_processor',
                password='testpass',
                role='root'
            )
        
        self.processor = MandayProcessor()
    
    def test_property_file_format_validation_csv(self):
        """
        Feature: mandays-overtime-summary, Property 1: File format validation
        Validates: Requirements 1.2, 1.4
        
        For any uploaded file with CSV extension, the system should accept it for processing
        """
        # Create a mock CSV file
        csv_content = "epNo,punchDate,mandays,regularMandayHr,ot\nEMP001,2024-01-01,1.00,8.00,0.00"
        
        class MockFile:
            def __init__(self, content, name):
                self.content = content
                self.name = name
                self.position = 0
            
            def read(self):
                return self.content.encode('utf-8')
            
            def seek(self, position):
                self.position = position
        
        mock_file = MockFile(csv_content, "test.csv")
        
        # Validate file
        result = self.processor.validate_csv(mock_file)
        
        # Should be valid
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['errors']), 0)
    
    def test_property_file_format_validation_invalid(self):
        """
        Feature: mandays-overtime-summary, Property 1: File format validation
        Validates: Requirements 1.2, 1.4
        
        For any uploaded file with invalid extension, the system should reject it
        """
        class MockFile:
            def __init__(self, name):
                self.name = name
            
            def read(self):
                return b"test content"
            
            def seek(self, position):
                pass
        
        mock_file = MockFile("test.txt")
        
        # Try to read file
        result = self.processor.read_file_to_dataframe(mock_file)
        
        # Should return None for unsupported format
        self.assertIsNone(result)
    
    def test_property_mandatory_column_presence(self):
        """
        Feature: mandays-overtime-summary, Property 2: Mandatory column presence
        Validates: Requirements 2.1, 2.2
        
        For any uploaded file missing mandatory columns, the system should reject it
        """
        # Create CSV with missing columns
        csv_content = "epNo,punchDate\nEMP001,2024-01-01"
        
        class MockFile:
            def __init__(self, content, name):
                self.content = content
                self.name = name
            
            def read(self):
                return self.content.encode('utf-8')
            
            def seek(self, position):
                pass
        
        mock_file = MockFile(csv_content, "test.csv")
        
        # Validate file
        result = self.processor.validate_csv(mock_file)
        
        # Should be invalid
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['errors']), 0)
        self.assertIn('Missing required fields', result['errors'][0])
    
    @settings(max_examples=50)
    @given(
        mandays=st.decimals(min_value=Decimal('0.00'), max_value=Decimal('99.99'), places=2),
        regular_hr=st.decimals(min_value=Decimal('0.00'), max_value=Decimal('99.99'), places=2),
        ot=st.decimals(min_value=Decimal('0.00'), max_value=Decimal('99.99'), places=2)
    )
    def test_property_numeric_data_type_preservation(self, mandays, regular_hr, ot):
        """
        Feature: mandays-overtime-summary, Property 6: Numeric data type preservation
        Validates: Requirements 3.4
        
        For any numeric field, the system should preserve the numeric data type and precision
        """
        # Validate decimal values
        mandays_result = self.processor.validate_decimal(mandays, 'mandays')
        regular_hr_result = self.processor.validate_decimal(regular_hr, 'regularMandayHr')
        ot_result = self.processor.validate_decimal(ot, 'ot')
        
        # All should be valid and preserve precision
        self.assertIsNotNone(mandays_result)
        self.assertIsNotNone(regular_hr_result)
        self.assertIsNotNone(ot_result)
        
        self.assertEqual(mandays_result, mandays)
        self.assertEqual(regular_hr_result, regular_hr)
        self.assertEqual(ot_result, ot)
    
    @settings(max_examples=50)
    @given(
        days_ago=st.integers(min_value=0, max_value=365)
    )
    def test_property_date_format_validation(self, days_ago):
        """
        Feature: mandays-overtime-summary, Property 9: Date format validation
        Validates: Requirements 5.2
        
        For any valid past date, the system should accept it
        """
        test_date = date.today() - timedelta(days=days_ago)
        
        # Test unambiguous date format (YYYY-MM-DD)
        date_str = test_date.strftime('%Y-%m-%d')
        result = self.processor.validate_date(date_str)
        self.assertIsNotNone(result)
        self.assertEqual(result, test_date)
    
    def test_property_future_date_rejected(self):
        """
        Feature: mandays-overtime-summary, Property 9: Date format validation
        Validates: Requirements 5.2
        
        For any future date, the system should reject it
        """
        future_date = date.today() + timedelta(days=30)
        future_date_str = future_date.strftime('%Y-%m-%d')
        
        result = self.processor.validate_date(future_date_str)
        
        # Should be None (rejected)
        self.assertIsNone(result)
    
    def test_property_optional_field_handling(self):
        """
        Feature: mandays-overtime-summary, Property 5: Optional field handling
        Validates: Requirements 3.3
        
        For any row with missing optional fields, the system should accept it and store NULL
        """
        row = {
            'epNo': 'EMP001',
            'punchDate': '2024-01-01',
            'mandays': '1.00',
            'regularMandayHr': '8.00',
            'ot': '0.00',
            # Optional fields not provided
        }
        
        success, error_msg, data = self.processor.process_row(row, 2, self.admin_user)
        
        # Should succeed
        self.assertTrue(success)
        self.assertIsNone(error_msg)
        
        # Optional fields should be None
        self.assertIsNone(data['trade'])
        self.assertIsNone(data['contract'])
        self.assertIsNone(data['plant'])
        self.assertIsNone(data['plant_desc'])
    
    def test_property_mandatory_field_validation(self):
        """
        Feature: mandays-overtime-summary, Property 3: Mandatory field validation
        Validates: Requirements 2.3, 2.4, 2.5
        
        For any row with empty mandatory fields, the system should reject it
        """
        # Test with missing epNo
        row = {
            'epNo': '',
            'punchDate': '2024-01-01',
            'mandays': '1.00',
            'regularMandayHr': '8.00',
            'ot': '0.00',
        }
        
        success, error_msg, data = self.processor.process_row(row, 2, self.admin_user)
        
        # Should fail
        self.assertFalse(success)
        self.assertIsNotNone(error_msg)
        self.assertIn('Missing required field', error_msg)
    
    def test_property_column_extraction(self):
        """
        Feature: mandays-overtime-summary, Property 4: Column extraction
        Validates: Requirements 3.1, 3.2
        
        For any file with extra columns, the system should extract only specified columns
        """
        # Create DataFrame with extra columns
        df = pd.DataFrame({
            'epNo': ['EMP001'],
            'punchDate': ['2024-01-01'],
            'mandays': [1.00],
            'regularMandayHr': [8.00],
            'ot': [0.00],
            'extraColumn1': ['extra'],
            'extraColumn2': ['data']
        })
        
        # Map columns
        column_mapping = self.processor.map_columns(df.columns.tolist())
        
        # Should only include expected columns
        expected_columns = ['epNo', 'punchDate', 'mandays', 'regularMandayHr', 'ot']
        for col in expected_columns:
            self.assertIn(col, column_mapping.values())
        
        # Should not include extra columns
        self.assertNotIn('extraColumn1', column_mapping.values())
        self.assertNotIn('extraColumn2', column_mapping.values())
    
    def test_negative_values_rejected(self):
        """Test that negative numeric values are rejected"""
        # Test negative mandays
        result = self.processor.validate_decimal(Decimal('-1.00'), 'mandays')
        self.assertIsNone(result)
        
        # Test negative regular hours
        result = self.processor.validate_decimal(Decimal('-8.00'), 'regularMandayHr')
        self.assertIsNone(result)
        
        # Test negative OT
        result = self.processor.validate_decimal(Decimal('-2.00'), 'ot')
        self.assertIsNone(result)


class MandayProcessorUnitTests(TestCase):
    """Unit tests for MandayProcessor"""
    
    def setUp(self):
        """Set up test data"""
        self.company = Company.objects.create(name="Test Unit Company")
        self.admin_user = User.objects.create_user(
            username='admin_unit',
            password='testpass',
            role='admin',
            company=self.company
        )
        self.processor = MandayProcessor()
    
    def test_column_aliases(self):
        """Test that column aliases are properly mapped"""
        # Test various alias formats
        test_columns = ['EP NO', 'PUNCH DATE', 'MANDAYS', 'REGULAR MANDAY HR', 'OT']
        
        mapping = self.processor.map_columns(test_columns)
        
        # Verify all columns are mapped
        self.assertIn('epNo', mapping.values())
        self.assertIn('punchDate', mapping.values())
        self.assertIn('mandays', mapping.values())
        self.assertIn('regularMandayHr', mapping.values())
        self.assertIn('ot', mapping.values())
    
    def test_create_or_update_record(self):
        """Test record creation and update"""
        data = {
            'ep_no': 'EMP001',
            'punch_date': date(2024, 1, 1),
            'mandays': Decimal('1.00'),
            'regular_manday_hr': Decimal('8.00'),
            'ot': Decimal('0.00'),
            'company': self.company,
            'trade': None,
            'contract': None,
            'plant': None,
            'plant_desc': None,
        }
        
        # Create record
        created, updated = self.processor.create_or_update_record(data)
        self.assertTrue(created)
        self.assertFalse(updated)
        
        # Update record
        data['mandays'] = Decimal('2.00')
        created, updated = self.processor.create_or_update_record(data)
        self.assertFalse(created)
        self.assertTrue(updated)
        
        # Verify update
        record = MandaySummaryRecord.objects.get(ep_no='EMP001', punch_date=date(2024, 1, 1))
        self.assertEqual(record.mandays, Decimal('2.00'))
