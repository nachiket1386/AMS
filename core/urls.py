"""
URL configuration for core app
"""
from django.urls import path
from . import views
from . import views_excel_api
from . import views_excel_query_api
from . import views_excel_export_api

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
    
    # Excel File Upload API
    path('api/excel/upload/', views_excel_api.upload_excel_file, name='api_excel_upload'),
    path('api/excel/upload/<str:session_id>/process/', views_excel_api.process_excel_file, name='api_excel_process'),
    path('api/excel/upload/<str:session_id>/progress/', views_excel_api.get_import_progress, name='api_excel_progress'),
    path('api/excel/upload/<str:session_id>/confirm/', views_excel_api.confirm_excel_import, name='api_excel_confirm'),
    path('api/excel/upload/<str:session_id>/errors/', views_excel_api.download_error_report, name='api_excel_errors'),
    path('api/excel/imports/', views_excel_api.import_history, name='api_excel_imports'),
    path('api/excel/imports/<int:import_id>/', views_excel_api.import_detail, name='api_excel_import_detail'),
    path('api/excel/permissions/', views_excel_api.manage_permissions, name='api_excel_permissions'),
    path('api/excel/audit/uploads/', views_excel_api.upload_audit_log, name='api_excel_audit'),
    
    # Excel Query API
    path('api/excel/attendance/', views_excel_query_api.query_attendance, name='api_excel_attendance'),
    path('api/excel/punch-records/', views_excel_query_api.query_punch_records, name='api_excel_punch_records'),
    path('api/excel/requests/', views_excel_query_api.query_requests, name='api_excel_requests'),
    path('api/excel/dashboard/', views_excel_query_api.dashboard_data, name='api_excel_dashboard'),
    
    # Excel Export API
    path('api/excel/export/', views_excel_export_api.export_data, name='api_excel_export'),
    path('api/excel/export/logs/', views_excel_export_api.export_logs, name='api_excel_export_logs'),
    
    # Excel UI Views
    path('excel/upload/', views.excel_upload_view, name='excel_upload'),
    path('excel/dashboard/', views.excel_dashboard_view, name='excel_dashboard'),
    path('excel/search/', views.excel_search_view, name='excel_search'),
    path('excel/history/', views.excel_import_history_view, name='excel_import_history'),
    path('excel/permissions/', views.excel_permissions_view, name='excel_permissions'),
    
    # Remarks Management
    path('attendance/<int:record_id>/add-remark/', views.add_remark_view, name='add_remark'),
    path('remarks/log/', views.remarks_log_view, name='remarks_log'),
    path('remarks/log/export/', views.export_remarks_log_view, name='export_remarks_log'),
    path('remarks/log/upload/', views.upload_remarks_log_view, name='upload_remarks_log'),
    path('remarks/manage-reasons/', views.manage_remark_reasons_view, name='manage_remark_reasons'),
    
    # Report Views
    path('reports/arc-summary/', views.arc_summary_report, name='arc_summary_report'),
    path('reports/overtime/', views.overtime_report, name='overtime_report'),
    path('reports/partial-day/', views.partial_day_report, name='partial_day_report'),
    path('reports/regularization/', views.regularization_report, name='regularization_report'),
]
