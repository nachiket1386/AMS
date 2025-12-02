"""
URL configuration for core app
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # Attendance Management
    path('attendance/', views.attendance_list_view, name='attendance_list'),
    path('attendance/export/', views.attendance_export_view, name='attendance_export'),
    path('attendance/<int:record_id>/edit/', views.attendance_edit_view, name='attendance_edit'),
    path('attendance/<int:record_id>/delete/', views.attendance_delete_view, name='attendance_delete'),
    path('attendance/delete-all/', views.attendance_delete_all_view, name='attendance_delete_all'),
    
    # CSV Upload
    path('upload/', views.upload_csv_view, name='upload'),
    path('upload/progress/', views.upload_progress_view, name='upload_progress'),
    path('upload/logs/', views.upload_logs_view, name='upload_logs'),
    path('upload/template/', views.download_csv_template, name='download_template'),
    
    # Export
    path('export/', views.export_csv_view, name='export'),
    
    # User Management
    path('users/', views.user_list_view, name='user_list'),
    path('users/create/', views.user_create_view, name='user_create'),
    path('users/<int:user_id>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<int:user_id>/delete/', views.user_delete_view, name='user_delete'),
    
    # Backup and Restore
    path('backup/', views.backup_data_view, name='backup_data'),
    path('backup/download/', views.download_backup_view, name='download_backup'),
    path('restore/', views.restore_data_view, name='restore_data'),
    path('restore/preview/', views.restore_preview_view, name='restore_preview'),
    path('restore/apply/', views.restore_apply_view, name='restore_apply'),
    
    # User1 Supervisor Management - Access Requests
    path('request-access/', views.request_access_view, name='request_access'),
    path('my-requests/', views.my_requests_view, name='my_requests'),
    path('cancel-request/<int:request_id>/', views.cancel_request_view, name='cancel_request'),
    
    # Admin - Approve Requests
    path('approve-requests/', views.approve_requests_view, name='approve_requests'),
    path('approve-request/<int:request_id>/', views.approve_request_action, name='approve_request'),
    path('reject-request/<int:request_id>/', views.reject_request_action, name='reject_request'),
    
    # Admin - Manage Assignments
    path('manage-assignments/', views.manage_assignments_view, name='manage_assignments'),
    path('remove-assignment/<int:assignment_id>/', views.remove_assignment_view, name='remove_assignment'),
]
