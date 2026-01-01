"""
Data models for the attendance management system
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class Company(models.Model):
    """Company model for multi-tenant data isolation"""
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Custom user model with role-based access control"""
    ROLE_CHOICES = [
        ('root', 'Root'),
        ('admin', 'Admin'),
        ('user1', 'User1'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user1')
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    # Date-based access control for User1
    assigned_date_from = models.DateField(null=True, blank=True, verbose_name='Access From Date')
    assigned_date_to = models.DateField(null=True, blank=True, verbose_name='Access To Date')

    class Meta:
        ordering = ['username']

    def clean(self):
        """Validate that Admin and User1 have a company assigned"""
        if self.role in ['admin', 'user1'] and not self.company:
            raise ValidationError('Admin and User1 roles must have a company assigned')
        
        # Validate date range for User1
        if self.role == 'user1':
            if self.assigned_date_from and self.assigned_date_to:
                if self.assigned_date_from > self.assigned_date_to:
                    raise ValidationError('Access From Date must be before Access To Date')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class AttendanceRecord(models.Model):
    """Attendance record for employees"""
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('PH', 'Public Holiday'),
        ('PD', 'Partial Day'),
        ('WO', 'Week Off'),
        ('-0.5', 'Half Day'),
        ('-1', 'Full Day Leave'),
    ]
    
    ep_no = models.CharField(max_length=50, verbose_name='Employee Number')
    ep_name = models.CharField(max_length=255, verbose_name='Employee Name')
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    date = models.DateField()
    shift = models.CharField(max_length=50, blank=True)
    overstay = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='P')
    
    # Optional time fields
    in_time = models.TimeField(null=True, blank=True, verbose_name='IN')
    out_time = models.TimeField(null=True, blank=True, verbose_name='OUT')
    in_time_2 = models.TimeField(null=True, blank=True, verbose_name='IN (2)')
    out_time_2 = models.TimeField(null=True, blank=True, verbose_name='OUT (2)')
    in_time_3 = models.TimeField(null=True, blank=True, verbose_name='IN (3)')
    out_time_3 = models.TimeField(null=True, blank=True, verbose_name='OUT (3)')
    hours = models.CharField(max_length=20, blank=True, verbose_name='HOURS')  # Store as HH:MM string
    overtime = models.TimeField(null=True, blank=True, verbose_name='OVERTIME')
    overtime_to_mandays = models.CharField(max_length=20, blank=True, verbose_name='OVERTIME TO MANDAYS')
    
    # ARC Summary specific fields
    cont_code = models.CharField(max_length=50, blank=True, verbose_name='Contractor Code')
    trade = models.CharField(max_length=100, blank=True, verbose_name='Trade')
    contract = models.CharField(max_length=100, blank=True, verbose_name='Contract')
    mandays = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Mandays')
    regular_manday_hr = models.CharField(max_length=20, blank=True, verbose_name='Regular Manday Hours')
    ot = models.CharField(max_length=20, blank=True, verbose_name='OT')
    
    # Overtime request fields
    actual_overstay = models.CharField(max_length=20, blank=True, verbose_name='Actual Overstay')
    requested_overtime = models.CharField(max_length=20, blank=True, verbose_name='Requested Overtime')
    approved_overtime = models.CharField(max_length=20, blank=True, verbose_name='Approved Overtime')
    requested_regular_manday_hours = models.CharField(max_length=20, blank=True, verbose_name='Requested Regular Manday Hours')
    approved_regular_manday_hours = models.CharField(max_length=20, blank=True, verbose_name='Approved Regular Manday Hours')
    contractor_ot_remarks = models.TextField(blank=True, verbose_name='Contractor OT Remarks')
    contractor_ot_reason = models.TextField(blank=True, verbose_name='Contractor OT Reason')
    requested_eic_code = models.CharField(max_length=50, blank=True, verbose_name='Requested EIC Code')
    requested_eic_name = models.CharField(max_length=255, blank=True, verbose_name='Requested EIC Name')
    ot_request_status = models.CharField(max_length=20, blank=True, verbose_name='OT Request Status')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['ep_no', 'date']
        ordering = ['-date', 'ep_no']
        indexes = [
            models.Index(fields=['ep_no', 'date']),
            models.Index(fields=['company', 'date']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.ep_no} - {self.ep_name} ({self.date})"


class UploadLog(models.Model):
    """Audit log for CSV upload operations"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='upload_logs'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    success_count = models.IntegerField(default=0)
    updated_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    error_messages = models.TextField(blank=True)

    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['user', 'uploaded_at']),
            models.Index(fields=['uploaded_at']),
        ]

    def __str__(self):
        return f"{self.filename} by {self.user.username} at {self.uploaded_at}"


class BackupLog(models.Model):
    """Audit log for backup and restore operations"""
    OPERATION_CHOICES = [
        ('backup_full', 'Full Backup'),
        ('backup_incremental', 'Incremental Backup'),
        ('restore', 'Restore'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='backup_logs'
    )
    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES)
    filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Statistics
    companies_count = models.IntegerField(default=0)
    records_count = models.IntegerField(default=0)
    records_added = models.IntegerField(default=0)  # For restore
    records_updated = models.IntegerField(default=0)  # For restore
    records_skipped = models.IntegerField(default=0)  # For restore
    
    # Status
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_operation_display()} - {self.filename} by {self.user.username} at {self.created_at}"


class EmployeeAssignment(models.Model):
    """Assignment of an employee to a User1 supervisor for access control"""
    SOURCE_CHOICES = [
        ('request', 'Access Request'),
        ('admin', 'Admin Assigned'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='employee_assignments',
        limit_choices_to={'role': 'user1'}
    )
    ep_no = models.CharField(max_length=50, verbose_name='Employee Number')
    ep_name = models.CharField(max_length=255, verbose_name='Employee Name')
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='employee_assignments'
    )
    
    # Date range (None = permanent access)
    access_from = models.DateField(
        null=True,
        blank=True,
        verbose_name='Access From Date',
        help_text='Leave blank for permanent access'
    )
    access_to = models.DateField(
        null=True,
        blank=True,
        verbose_name='Access To Date',
        help_text='Leave blank for permanent access'
    )
    
    # Metadata
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assignments_created',
        verbose_name='Assigned By'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(
        max_length=10,
        choices=SOURCE_CHOICES,
        default='admin',
        help_text='How this assignment was created'
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-assigned_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['ep_no', 'is_active']),
            models.Index(fields=['company', 'is_active']),
        ]
    
    def clean(self):
        """Validate date range"""
        if self.access_from and self.access_to:
            if self.access_from > self.access_to:
                raise ValidationError('Access From Date must be before Access To Date')
    
    def is_active_on_date(self, check_date=None):
        """
        Check if assignment is active on a specific date
        
        Args:
            check_date: Date to check (defaults to today)
            
        Returns:
            bool: True if assignment is active on the given date
        """
        from django.utils import timezone
        
        if not self.is_active:
            return False
        
        if check_date is None:
            check_date = timezone.now().date()
        
        # Permanent access (no date restrictions)
        if not self.access_from and not self.access_to:
            return True
        
        # Check if date falls within range
        if self.access_from and check_date < self.access_from:
            return False
        
        if self.access_to and check_date > self.access_to:
            return False
        
        return True
    
    def get_date_range_display(self):
        """
        Get human-readable date range
        
        Returns:
            str: Formatted date range or "Permanent"
        """
        if not self.access_from and not self.access_to:
            return "Permanent"
        
        if self.access_from and self.access_to:
            return f"{self.access_from.strftime('%Y-%m-%d')} to {self.access_to.strftime('%Y-%m-%d')}"
        
        if self.access_from:
            return f"From {self.access_from.strftime('%Y-%m-%d')}"
        
        if self.access_to:
            return f"Until {self.access_to.strftime('%Y-%m-%d')}"
        
        return "Permanent"
    
    def __str__(self):
        return f"{self.user.username} → {self.ep_no} ({self.get_date_range_display()})"


class AccessRequest(models.Model):
    """Request from User1 to access employee data"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    ACCESS_TYPE_CHOICES = [
        ('date_range', 'Date Range'),
        ('permanent', 'Permanent'),
    ]
    
    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='access_requests',
        limit_choices_to={'role': 'user1'}
    )
    ep_no = models.CharField(max_length=50, verbose_name='Employee Number')
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='access_requests'
    )
    
    # Access details
    access_type = models.CharField(
        max_length=20,
        choices=ACCESS_TYPE_CHOICES,
        default='date_range'
    )
    access_from = models.DateField(
        null=True,
        blank=True,
        verbose_name='Access From Date'
    )
    access_to = models.DateField(
        null=True,
        blank=True,
        verbose_name='Access To Date'
    )
    justification = models.TextField(
        help_text='Reason for requesting access'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Approval/Rejection
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_requests',
        verbose_name='Reviewed By'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['requester', 'status']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['ep_no', 'status']),
        ]
    
    def clean(self):
        """Validate request data"""
        # Date range requests must have dates
        if self.access_type == 'date_range':
            if not self.access_from or not self.access_to:
                raise ValidationError('Date range access requires both start and end dates')
            if self.access_from > self.access_to:
                raise ValidationError('Access From Date must be before Access To Date')
    
    def can_cancel(self):
        """Check if request can be cancelled by requester"""
        return self.status == 'pending'
    
    def can_approve(self):
        """Check if request can be approved by admin"""
        return self.status == 'pending'
    
    def can_reject(self):
        """Check if request can be rejected by admin"""
        return self.status == 'pending'
    
    def __str__(self):
        return f"{self.requester.username} → {self.ep_no} ({self.get_status_display()})"


class AccessRequestAuditLog(models.Model):
    """Audit log for access requests and assignment changes"""
    ACTION_CHOICES = [
        ('request_created', 'Request Created'),
        ('request_approved', 'Request Approved'),
        ('request_rejected', 'Request Rejected'),
        ('request_cancelled', 'Request Cancelled'),
        ('assignment_created', 'Assignment Created'),
        ('assignment_removed', 'Assignment Removed'),
        ('assignment_expired', 'Assignment Expired'),
    ]
    
    timestamp = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_actions',
        help_text='User who performed the action'
    )
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    
    # Target information
    target_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_targets',
        help_text='User1 affected by this action'
    )
    target_ep_no = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Employee Number'
    )
    
    # Additional details (JSON-serializable data)
    details = models.JSONField(
        default=dict,
        blank=True,
        help_text='Additional context about the action'
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['actor', 'timestamp']),
            models.Index(fields=['target_user', 'timestamp']),
            models.Index(fields=['target_ep_no', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
        ]
    
    @classmethod
    def create_log_entry(cls, action, actor=None, target_user=None, target_ep_no='', details=None):
        """
        Create an audit log entry
        
        Args:
            action: Action type from ACTION_CHOICES
            actor: User who performed the action
            target_user: User1 affected by the action
            target_ep_no: Employee number involved
            details: Additional context (dict)
            
        Returns:
            AccessRequestAuditLog: Created log entry
        """
        return cls.objects.create(
            action=action,
            actor=actor,
            target_user=target_user,
            target_ep_no=target_ep_no,
            details=details or {}
        )
    
    def __str__(self):
        actor_name = self.actor.username if self.actor else 'System'
        return f"{self.get_action_display()} by {actor_name} at {self.timestamp}"


# ============================================================================
# Excel File Upload Integration Models
# ============================================================================

class Employee(models.Model):
    """Employee master table for Excel upload integration"""
    ep_no = models.CharField(max_length=12, primary_key=True, verbose_name='Employee Number')
    ep_name = models.CharField(max_length=255, verbose_name='Employee Name')
    contractor = models.ForeignKey(
        'Contractor',
        on_delete=models.PROTECT,
        related_name='employees'
    )
    sector_name = models.CharField(max_length=100, blank=True)
    plant_name = models.CharField(max_length=100, blank=True)
    department_name = models.CharField(max_length=100, blank=True)
    trade_name = models.CharField(max_length=100, blank=True)
    skill = models.CharField(max_length=50, blank=True)
    card_category = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'employees'
        ordering = ['ep_no']
        indexes = [
            models.Index(fields=['contractor']),
            models.Index(fields=['plant_name']),
            models.Index(fields=['sector_name']),
        ]
    
    def __str__(self):
        return f"{self.ep_no} - {self.ep_name}"


class Contractor(models.Model):
    """Contractor master table for Excel upload integration"""
    contractor_code = models.IntegerField(primary_key=True, verbose_name='Contractor Code')
    contractor_name = models.CharField(max_length=255, verbose_name='Contractor Name')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contractors'
        ordering = ['contractor_code']
    
    def __str__(self):
        return f"{self.contractor_code} - {self.contractor_name}"


class Plant(models.Model):
    """Plant master table for Excel upload integration"""
    plant_code = models.CharField(max_length=50, primary_key=True, verbose_name='Plant Code')
    plant_name = models.CharField(max_length=255, verbose_name='Plant Name')
    sector_name = models.CharField(max_length=100, blank=True)
    site_code = models.CharField(max_length=50, blank=True)
    site_desc = models.CharField(max_length=255, blank=True, verbose_name='Site Description')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'plants'
        ordering = ['plant_code']
    
    def __str__(self):
        return f"{self.plant_code} - {self.plant_name}"



class PunchRecord(models.Model):
    """Punch record transaction table for Excel upload integration"""
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='punch_records'
    )
    punchdate = models.DateField(verbose_name='Punch Date')
    shift = models.CharField(max_length=50, blank=True)
    punch1_in = models.TimeField(null=True, blank=True, verbose_name='Punch 1 IN')
    punch2_out = models.TimeField(null=True, blank=True, verbose_name='Punch 2 OUT')
    punch3_in = models.TimeField(null=True, blank=True, verbose_name='Punch 3 IN')
    punch4_out = models.TimeField(null=True, blank=True, verbose_name='Punch 4 OUT')
    punch5_in = models.TimeField(null=True, blank=True, verbose_name='Punch 5 IN')
    punch6_out = models.TimeField(null=True, blank=True, verbose_name='Punch 6 OUT')
    early_in = models.TimeField(null=True, blank=True, verbose_name='Early IN')
    late_come = models.TimeField(null=True, blank=True, verbose_name='Late Come')
    early_out = models.TimeField(null=True, blank=True, verbose_name='Early OUT')
    hours_worked = models.TimeField(null=True, blank=True, verbose_name='Hours Worked')
    overstay = models.TimeField(null=True, blank=True, verbose_name='Overstay')
    overtime = models.TimeField(null=True, blank=True, verbose_name='Overtime')
    status = models.CharField(max_length=10, verbose_name='Status')
    regular_hours = models.TimeField(null=True, blank=True, verbose_name='Regular Hours')
    manual_request = models.BooleanField(default=False, verbose_name='Manual Request')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'punch_records'
        unique_together = [['employee', 'punchdate']]
        ordering = ['-punchdate', 'employee']
        indexes = [
            models.Index(fields=['punchdate']),
            models.Index(fields=['employee', 'punchdate']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.employee.ep_no} - {self.punchdate}"


class DailySummary(models.Model):
    """Daily summary table for Excel upload integration"""
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='daily_summaries'
    )
    punchdate = models.DateField(verbose_name='Punch Date')
    mandays = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Mandays')
    regular_manday_hr = models.TimeField(null=True, blank=True, verbose_name='Regular Manday Hours')
    ot = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Overtime')
    location_status = models.CharField(max_length=50, blank=True, verbose_name='Location Status')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'daily_summary'
        unique_together = [['employee', 'punchdate']]
        ordering = ['-punchdate', 'employee']
        indexes = [
            models.Index(fields=['punchdate']),
            models.Index(fields=['employee', 'punchdate']),
        ]
        verbose_name_plural = 'Daily Summaries'
    
    def __str__(self):
        return f"{self.employee.ep_no} - {self.punchdate}"


class OvertimeRequest(models.Model):
    """Overtime request table for Excel upload integration"""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='overtime_requests'
    )
    punchdate = models.DateField(verbose_name='Punch Date')
    actual_overstay = models.TimeField(null=True, blank=True, verbose_name='Actual Overstay')
    requested_overtime = models.TimeField(null=True, blank=True, verbose_name='Requested Overtime')
    approved_overtime = models.TimeField(null=True, blank=True, verbose_name='Approved Overtime')
    requested_regular_hours = models.TimeField(null=True, blank=True, verbose_name='Requested Regular Hours')
    approved_regular_hours = models.TimeField(null=True, blank=True, verbose_name='Approved Regular Hours')
    contractor_request_date = models.DateTimeField(null=True, blank=True, verbose_name='Contractor Request Date')
    contractor_remarks = models.TextField(blank=True, verbose_name='Contractor Remarks')
    contractor_reason = models.TextField(blank=True, verbose_name='Contractor Reason')
    actual_eic_code = models.IntegerField(null=True, blank=True, verbose_name='Actual EIC Code')
    requested_eic_code = models.IntegerField(null=True, blank=True, verbose_name='Requested EIC Code')
    eic_approve_date = models.DateTimeField(null=True, blank=True, verbose_name='EIC Approve Date')
    eic_remarks = models.TextField(blank=True, verbose_name='EIC Remarks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'overtime_requests'
        unique_together = [['employee', 'punchdate']]
        ordering = ['-punchdate', 'employee']
        indexes = [
            models.Index(fields=['punchdate']),
            models.Index(fields=['employee', 'punchdate']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.employee.ep_no} - {self.punchdate} ({self.status})"


class PartialDayRequest(models.Model):
    """Partial day request table for Excel upload integration"""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='partial_day_requests'
    )
    punchdate = models.DateField(verbose_name='Punch Date')
    actual_pd_hours = models.TimeField(null=True, blank=True, verbose_name='Actual PD Hours')
    requested_pd_hours = models.TimeField(null=True, blank=True, verbose_name='Requested PD Hours')
    approved_pd_hours = models.TimeField(null=True, blank=True, verbose_name='Approved PD Hours')
    manday_conversion = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Manday Conversion')
    contractor_request_date = models.DateTimeField(null=True, blank=True, verbose_name='Contractor Request Date')
    contractor_remarks = models.TextField(blank=True, verbose_name='Contractor Remarks')
    eic_code = models.IntegerField(null=True, blank=True, verbose_name='EIC Code')
    eic_approve_date = models.DateTimeField(null=True, blank=True, verbose_name='EIC Approve Date')
    eic_remarks = models.TextField(blank=True, verbose_name='EIC Remarks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'partial_day_requests'
        unique_together = [['employee', 'punchdate']]
        ordering = ['-punchdate', 'employee']
        indexes = [
            models.Index(fields=['punchdate']),
            models.Index(fields=['employee', 'punchdate']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.employee.ep_no} - {self.punchdate} ({self.status})"


class RegularizationRequest(models.Model):
    """Regularization request table for Excel upload integration"""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='regularization_requests'
    )
    punchdate = models.DateField(verbose_name='Punch Date')
    old_punch_in = models.TimeField(null=True, blank=True, verbose_name='Old Punch IN')
    old_punch_out = models.TimeField(null=True, blank=True, verbose_name='Old Punch OUT')
    new_punch_in = models.TimeField(null=True, blank=True, verbose_name='New Punch IN')
    new_punch_out = models.TimeField(null=True, blank=True, verbose_name='New Punch OUT')
    contractor_request_date = models.DateTimeField(null=True, blank=True, verbose_name='Contractor Request Date')
    contractor_remarks = models.TextField(blank=True, verbose_name='Contractor Remarks')
    contractor_reason = models.TextField(blank=True, verbose_name='Contractor Reason')
    eic_code = models.IntegerField(null=True, blank=True, verbose_name='EIC Code')
    eic_approve_date = models.DateTimeField(null=True, blank=True, verbose_name='EIC Approve Date')
    eic_remarks = models.TextField(blank=True, verbose_name='EIC Remarks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'regularization_requests'
        unique_together = [['employee', 'punchdate']]
        ordering = ['-punchdate', 'employee']
        indexes = [
            models.Index(fields=['punchdate']),
            models.Index(fields=['employee', 'punchdate']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.employee.ep_no} - {self.punchdate} ({self.status})"



class ImportLog(models.Model):
    """Import log for Excel file uploads"""
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='excel_import_logs'
    )
    filename = models.CharField(max_length=255, verbose_name='Filename')
    file_type = models.CharField(max_length=50, verbose_name='File Type')
    total_rows = models.IntegerField(verbose_name='Total Rows')
    imported_rows = models.IntegerField(verbose_name='Imported Rows')
    duplicate_rows = models.IntegerField(verbose_name='Duplicate Rows')
    error_rows = models.IntegerField(verbose_name='Error Rows')
    status = models.CharField(max_length=20, verbose_name='Status')
    error_report_path = models.CharField(max_length=500, blank=True, verbose_name='Error Report Path')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'import_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['created_at']),
            models.Index(fields=['file_type']),
        ]
    
    def __str__(self):
        return f"{self.filename} - {self.status} ({self.created_at})"


class ExportLog(models.Model):
    """Export log for data exports"""
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='excel_export_logs'
    )
    export_type = models.CharField(max_length=50, verbose_name='Export Type')
    record_count = models.IntegerField(verbose_name='Record Count')
    filters = models.JSONField(default=dict, blank=True, verbose_name='Filters')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'export_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.export_type} - {self.record_count} records ({self.created_at})"


class UploadPermission(models.Model):
    """Upload permission for users"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='excel_upload_permissions'
    )
    file_type = models.CharField(max_length=50, verbose_name='File Type')
    can_upload = models.BooleanField(default=False, verbose_name='Can Upload')
    granted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='granted_permissions'
    )
    granted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'upload_permissions'
        unique_together = [['user', 'file_type']]
        ordering = ['-granted_at']
        indexes = [
            models.Index(fields=['user', 'file_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.file_type} ({'Allowed' if self.can_upload else 'Denied'})"


class RemarkReason(models.Model):
    """Remark reasons/categories managed by Admin"""
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='remark_reasons'
    )
    reason = models.CharField(max_length=255, verbose_name='Reason/Category')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_reasons'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'remark_reasons'
        ordering = ['reason']
        unique_together = ['company', 'reason']
        indexes = [
            models.Index(fields=['company', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.reason} ({self.company.name})"


class AttendanceRemark(models.Model):
    """Remarks added by User1 for attendance records"""
    attendance_record = models.ForeignKey(
        'AttendanceRecord',
        on_delete=models.CASCADE,
        related_name='remarks'
    )
    ep_no = models.CharField(max_length=50, verbose_name='EP Number')
    date = models.DateField(verbose_name='Attendance Date')
    reason = models.ForeignKey(
        RemarkReason,
        on_delete=models.SET_NULL,
        null=True,
        related_name='remarks'
    )
    remarks_text = models.TextField(verbose_name='Remarks/Comments')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_remarks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Admin response
    admin_response = models.TextField(blank=True, verbose_name='Admin Response')
    responded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='responded_remarks'
    )
    responded_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('reviewed', 'Reviewed'),
            ('resolved', 'Resolved'),
        ],
        default='pending'
    )
    
    class Meta:
        db_table = 'attendance_remarks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ep_no', 'date']),
            models.Index(fields=['created_by', 'created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['attendance_record']),
        ]
    
    def __str__(self):
        return f"{self.ep_no} - {self.date} - {self.reason}"
