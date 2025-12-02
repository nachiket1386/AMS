"""
Unit tests for the attendance management system
"""
from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, time as dt_time
from io import BytesIO
from .models import User, Company, AttendanceRecord, UploadLog
from .csv_processor import CSVProcessor


class CSVProcessorTestCase(TestCase):
    """Test cases for CSV processor"""
    
    def setUp(self):
        """Set up test data"""
        self.company = Company.objects.create(name='Test Company')
        self.root_user = User.objects.create_user(
            username='root',
            password='root123',
            role='root'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            role='admin',
            company=self.company
        )
        self.processor = CSVProcessor()
    
    def test_validate_date_valid(self):
        """Test date validation with valid date"""
        result = self.processor.validate_date('2024-01-15')
        self.assertIsNotNone(result)
        self.assertEqual(result, date(2024, 1, 15))
    
    def test_validate_date_invalid_format(self):
        """Test date validation with invalid format"""
        result = self.processor.validate_date('15-01-2024')
        self.assertIsNone(result)
    
    def test_validate_date_future(self):
        """Test date validation with future date"""
        result = self.processor.validate_date('2099-12-31')
        self.assertIsNone(result)
    
    def test_validate_date_empty(self):
        """Test date validation with empty string"""
        result = self.processor.validate_date('')
        self.assertIsNone(result)
    
    def test_validate_time_valid(self):
        """Test time validation with valid time"""
        result = self.processor.validate_time('09:30')
        self.assertIsNotNone(result)
        self.assertEqual(result, dt_time(9, 30))
    
    def test_validate_time_invalid_format(self):
        """Test time validation with invalid format"""
        result = self.processor.validate_time('9:30 AM')
        self.assertIsNone(result)
    
    def test_validate_time_empty(self):
        """Test time validation with empty string"""
        result = self.processor.validate_time('')
        self.assertIsNone(result)
    
    def test_validate_time_null(self):
        """Test time validation with None"""
        result = self.processor.validate_time(None)
        self.assertIsNone(result)
    
    def test_validate_status_valid(self):
        """Test status validation with valid values"""
        for status in ['P', 'A', 'PH', '-0.5', '-1']:
            result = self.processor.validate_status(status)
            self.assertTrue(result, f"Status {status} should be valid")
    
    def test_validate_status_invalid(self):
        """Test status validation with invalid values"""
        for status in ['X', 'Present', '0', '']:
            result = self.processor.validate_status(status)
            self.assertFalse(result, f"Status {status} should be invalid")
    
    def test_create_or_update_record_create(self):
        """Test creating a new record"""
        data = {
            'ep_no': 'EMP001',
            'ep_name': 'John Doe',
            'company': self.company,
            'date': date(2024, 1, 15),
            'shift': 'Day',
            'overstay': 'No',
            'status': 'P',
            'in_time': dt_time(9, 0),
            'out_time': dt_time(17, 0),
            'in_time_2': None,
            'out_time_2': None,
            'in_time_3': None,
            'out_time_3': None,
            'overtime': None,
            'overtime_to_mandays': None,
        }
        
        created, updated = self.processor.create_or_update_record(data)
        self.assertTrue(created)
        self.assertFalse(updated)
        
        # Verify record exists
        record = AttendanceRecord.objects.get(ep_no='EMP001', date=date(2024, 1, 15))
        self.assertEqual(record.ep_name, 'John Doe')
    
    def test_create_or_update_record_update(self):
        """Test updating an existing record"""
        # Create initial record
        AttendanceRecord.objects.create(
            ep_no='EMP001',
            ep_name='John Doe',
            company=self.company,
            date=date(2024, 1, 15),
            shift='Day',
            overstay='No',
            status='P'
        )
        
        # Update with new data
        data = {
            'ep_no': 'EMP001',
            'ep_name': 'John Smith',  # Changed name
            'company': self.company,
            'date': date(2024, 1, 15),
            'shift': 'Night',  # Changed shift
            'overstay': 'Yes',  # Changed overstay
            'status': 'A',  # Changed status
            'in_time': None,
            'out_time': None,
            'in_time_2': None,
            'out_time_2': None,
            'in_time_3': None,
            'out_time_3': None,
            'overtime': None,
            'overtime_to_mandays': None,
        }
        
        created, updated = self.processor.create_or_update_record(data)
        self.assertFalse(created)
        self.assertTrue(updated)
        
        # Verify record was updated
        record = AttendanceRecord.objects.get(ep_no='EMP001', date=date(2024, 1, 15))
        self.assertEqual(record.ep_name, 'John Smith')
        self.assertEqual(record.shift, 'Night')
        self.assertEqual(record.status, 'A')


class ModelTestCase(TestCase):
    """Test cases for models"""
    
    def setUp(self):
        """Set up test data"""
        self.company = Company.objects.create(name='Test Company')
    
    def test_company_creation(self):
        """Test company model creation"""
        company = Company.objects.create(name='New Company')
        self.assertEqual(str(company), 'New Company')
        self.assertIsNotNone(company.created_at)
    
    def test_company_unique_name(self):
        """Test company name uniqueness"""
        Company.objects.create(name='Unique Company')
        with self.assertRaises(Exception):
            Company.objects.create(name='Unique Company')
    
    def test_user_creation(self):
        """Test user model creation"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass',
            role='admin',
            company=self.company
        )
        self.assertEqual(user.role, 'admin')
        self.assertEqual(user.company, self.company)
    
    def test_attendance_record_unique_constraint(self):
        """Test attendance record unique constraint on ep_no and date"""
        AttendanceRecord.objects.create(
            ep_no='EMP001',
            ep_name='John Doe',
            company=self.company,
            date=date(2024, 1, 15),
            shift='Day',
            overstay='No',
            status='P'
        )
        
        # Try to create duplicate
        with self.assertRaises(Exception):
            AttendanceRecord.objects.create(
                ep_no='EMP001',
                ep_name='Jane Doe',
                company=self.company,
                date=date(2024, 1, 15),
                shift='Night',
                overstay='No',
                status='A'
            )


class AuthenticationTestCase(TestCase):
    """Test cases for authentication"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.company = Company.objects.create(name='Test Company')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            role='admin',
            company=self.company
        )
    
    def test_login_view_get(self):
        """Test login view GET request"""
        response = self.client.get(reverse('core:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_view_post_valid(self):
        """Test login view POST with valid credentials"""
        response = self.client.post(reverse('core:login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
    
    def test_login_view_post_invalid(self):
        """Test login view POST with invalid credentials"""
        response = self.client.post(reverse('core:login'), {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page
    
    def test_logout_view(self):
        """Test logout view"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('core:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout



class IntegrationTestCase(TestCase):
    """Integration tests for complete workflows"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.company1 = Company.objects.create(name='Test Company 1')
        self.company2 = Company.objects.create(name='Test Company 2')
        
        self.root_user = User.objects.create_user(
            username='root',
            password='root123',
            role='root',
            is_staff=True,
            is_superuser=True
        )
        
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            role='admin',
            company=self.company1
        )
        
        self.user1 = User.objects.create_user(
            username='user1',
            password='user123',
            role='user1',
            company=self.company1
        )
    
    def test_complete_upload_workflow_root(self):
        """Test complete CSV upload workflow for root user"""
        self.client.login(username='root', password='root123')
        
        # Create CSV content
        csv_content = """EP NO,EP NAME,COMPANY NAME,DATE,SHIFT,OVERSTAY,STATUS,IN,OUT
EMP001,John Doe,Test Company 1,2024-11-01,Day,No,P,09:00,17:00
EMP002,Jane Smith,Test Company 2,2024-11-01,Day,No,P,09:00,17:00"""
        
        from io import BytesIO
        csv_file = BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'test.csv'
        
        # Upload CSV
        response = self.client.post(reverse('core:upload'), {
            'csv_file': csv_file
        })
        
        # Verify records created
        self.assertEqual(AttendanceRecord.objects.count(), 2)
        self.assertEqual(UploadLog.objects.count(), 1)
    
    def test_complete_upload_workflow_admin(self):
        """Test CSV upload workflow for admin user"""
        self.client.login(username='admin', password='admin123')
        
        # Create CSV with own company
        csv_content = """EP NO,EP NAME,COMPANY NAME,DATE,SHIFT,OVERSTAY,STATUS
EMP001,John Doe,Test Company 1,2024-11-01,Day,No,P"""
        
        from io import BytesIO
        csv_file = BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'test.csv'
        
        response = self.client.post(reverse('core:upload'), {
            'csv_file': csv_file
        })
        
        # Verify record created
        self.assertEqual(AttendanceRecord.objects.filter(company=self.company1).count(), 1)
    
    def test_data_management_workflow(self):
        """Test view, edit, delete workflow"""
        self.client.login(username='admin', password='admin123')
        
        # Create record
        record = AttendanceRecord.objects.create(
            ep_no='EMP001',
            ep_name='John Doe',
            company=self.company1,
            date=date(2024, 11, 1),
            shift='Day',
            overstay='No',
            status='P'
        )
        
        # View list
        response = self.client.get(reverse('core:attendance_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'EMP001')
        
        # Edit record
        response = self.client.post(reverse('core:attendance_edit', args=[record.id]), {
            'ep_no': 'EMP001',
            'ep_name': 'John Smith',  # Changed
            'company': self.company1.id,
            'date': '2024-11-01',
            'shift': 'Night',  # Changed
            'overstay': 'No',
            'status': 'P'
        })
        
        record.refresh_from_db()
        self.assertEqual(record.ep_name, 'John Smith')
        self.assertEqual(record.shift, 'Night')
        
        # Delete record
        response = self.client.post(reverse('core:attendance_delete', args=[record.id]))
        self.assertEqual(AttendanceRecord.objects.count(), 0)
    
    def test_user_management_workflow(self):
        """Test user creation and editing"""
        self.client.login(username='root', password='root123')
        
        # Create user
        response = self.client.post(reverse('core:user_create'), {
            'username': 'newuser',
            'password': 'newpass123',
            'role': 'user1',
            'company': self.company1.id,
            'is_active': True
        })
        
        # Verify user created
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.role, 'user1')
        self.assertEqual(new_user.company, self.company1)
        
        # Edit user
        response = self.client.post(reverse('core:user_edit', args=[new_user.id]), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'user1',
            'company': self.company1.id,
            'is_active': True
        })
        
        new_user.refresh_from_db()
        self.assertEqual(new_user.first_name, 'New')
    
    def test_export_functionality(self):
        """Test data export with filters"""
        self.client.login(username='admin', password='admin123')
        
        # Create records
        AttendanceRecord.objects.create(
            ep_no='EMP001',
            ep_name='John Doe',
            company=self.company1,
            date=date(2024, 11, 1),
            shift='Day',
            overstay='No',
            status='P'
        )
        
        # Export
        response = self.client.get(reverse('core:export'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment', response['Content-Disposition'])
    
    def test_permission_enforcement(self):
        """Test permission enforcement across views"""
        # User1 should not access upload
        self.client.login(username='user1', password='user123')
        response = self.client.get(reverse('core:upload'))
        self.assertEqual(response.status_code, 403)
        
        # User1 should not edit records
        record = AttendanceRecord.objects.create(
            ep_no='EMP001',
            ep_name='John Doe',
            company=self.company1,
            date=date(2024, 11, 1),
            shift='Day',
            overstay='No',
            status='P'
        )
        response = self.client.get(reverse('core:attendance_edit', args=[record.id]))
        self.assertEqual(response.status_code, 403)
        
        # Admin should not access other company records
        self.client.login(username='admin', password='admin123')
        record2 = AttendanceRecord.objects.create(
            ep_no='EMP002',
            ep_name='Jane Smith',
            company=self.company2,
            date=date(2024, 11, 1),
            shift='Day',
            overstay='No',
            status='P'
        )
        response = self.client.get(reverse('core:attendance_edit', args=[record2.id]))
        self.assertEqual(response.status_code, 403)
