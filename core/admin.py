"""
Django admin configuration
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Company, AttendanceRecord, UploadLog


class CustomUserAdmin(BaseUserAdmin):
    """Custom admin for User model"""
    list_display = ('username', 'email', 'role', 'company', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'company')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'company')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'company')}),
    )
    
    def has_module_permission(self, request):
        """Only root users can access admin"""
        if request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role == 'root'):
            return True
        return False


class CompanyAdmin(admin.ModelAdmin):
    """Admin for Company model"""
    list_display = ('name', 'created_at', 'user_count', 'record_count')
    search_fields = ('name',)
    readonly_fields = ('created_at',)
    
    def user_count(self, obj):
        return obj.users.count()
    user_count.short_description = 'Users'
    
    def record_count(self, obj):
        return obj.attendance_records.count()
    record_count.short_description = 'Records'
    
    def has_module_permission(self, request):
        """Only root users can access admin"""
        if request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role == 'root'):
            return True
        return False


class AttendanceRecordAdmin(admin.ModelAdmin):
    """Admin for AttendanceRecord model"""
    list_display = ('ep_no', 'ep_name', 'company', 'date', 'shift', 'status', 'created_at')
    list_filter = ('status', 'company', 'date', 'shift')
    search_fields = ('ep_no', 'ep_name', 'company__name')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('ep_no', 'ep_name', 'company')
        }),
        ('Attendance Details', {
            'fields': ('date', 'shift', 'overstay', 'status')
        }),
        ('Time Details', {
            'fields': ('in_time', 'out_time', 'in_time_2', 'out_time_2', 'in_time_3', 'out_time_3')
        }),
        ('Overtime', {
            'fields': ('overtime', 'overtime_to_mandays')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_module_permission(self, request):
        """Only root users can access admin"""
        if request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role == 'root'):
            return True
        return False


class UploadLogAdmin(admin.ModelAdmin):
    """Admin for UploadLog model"""
    list_display = ('filename', 'user', 'uploaded_at', 'success_count', 'updated_count', 'error_count')
    list_filter = ('uploaded_at', 'user')
    search_fields = ('filename', 'user__username')
    date_hierarchy = 'uploaded_at'
    readonly_fields = ('user', 'uploaded_at', 'filename', 'success_count', 'updated_count', 'error_count', 'error_messages')
    
    fieldsets = (
        ('Upload Information', {
            'fields': ('user', 'filename', 'uploaded_at')
        }),
        ('Results', {
            'fields': ('success_count', 'updated_count', 'error_count')
        }),
        ('Error Details', {
            'fields': ('error_messages',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Disable adding upload logs through admin"""
        return False
    
    def has_module_permission(self, request):
        """Only root users can access admin"""
        if request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role == 'root'):
            return True
        return False


# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(AttendanceRecord, AttendanceRecordAdmin)
admin.site.register(UploadLog, UploadLogAdmin)

# Customize admin site
admin.site.site_header = 'Attendance Management System'
admin.site.site_title = 'Attendance Admin'
admin.site.index_title = 'System Administration'
