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
    shift = models.CharField(max_length=50)
    overstay = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    # Optional time fields
    in_time = models.TimeField(null=True, blank=True, verbose_name='IN')
    out_time = models.TimeField(null=True, blank=True, verbose_name='OUT')
    in_time_2 = models.TimeField(null=True, blank=True, verbose_name='IN (2)')
    out_time_2 = models.TimeField(null=True, blank=True, verbose_name='OUT (2)')
    in_time_3 = models.TimeField(null=True, blank=True, verbose_name='IN (3)')
    out_time_3 = models.TimeField(null=True, blank=True, verbose_name='OUT (3)')
    overtime = models.TimeField(null=True, blank=True, verbose_name='OVERTIME')
    overtime_to_mandays = models.TimeField(null=True, blank=True, verbose_name='OVERTIME TO MANDAYS')
    
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
