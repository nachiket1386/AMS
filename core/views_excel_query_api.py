"""
Query API Views for Excel File Upload Integration

This module provides REST API endpoints for querying attendance data with role-based filtering.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum
from datetime import datetime, timedelta
import logging

from core.models import (
    PunchRecord, DailySummary, OvertimeRequest, PartialDayRequest, RegularizationRequest,
    Employee, Contractor
)
from core.services.permission_service import PermissionService

logger = logging.getLogger(__name__)

# Initialize services
permission_service = PermissionService()


@login_required
@require_http_methods(["GET"])
def query_attendance(request):
    """
    Query attendance data with filters and role-based access
    
    GET /api/excel/attendance/
    Query params: ep_no, employee_name, date_from, date_to, status, page, page_size
    """
    try:
        # Get query parameters
        ep_no = request.GET.get('ep_no', '').strip()
        employee_name = request.GET.get('employee_name', '').strip()
        date_from = request.GET.get('date_from', '')
        date_to = request.GET.get('date_to', '')
        status = request.GET.get('status', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 50))
        
        # Start with all punch records
        queryset = PunchRecord.objects.select_related('employee', 'employee__contractor')
        
        # Apply role-based filtering
        queryset = permission_service.filter_queryset(queryset, request.user)
        
        # Apply filters
        if ep_no:
            queryset = queryset.filter(employee__ep_no__icontains=ep_no)
        
        if employee_name:
            queryset = queryset.filter(employee__ep_name__icontains=employee_name)
        
        if date_from:
            queryset = queryset.filter(punchdate__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(punchdate__lte=date_to)
        
        if status:
            queryset = queryset.filter(status=status)
        
        # Get total count
        total = queryset.count()
        
        # Paginate
        start = (page - 1) * page_size
        end = start + page_size
        records = queryset[start:end]
        
        # Serialize
        data = []
        for record in records:
            data.append({
                'id': record.id,
                'ep_no': record.employee.ep_no,
                'ep_name': record.employee.ep_name,
                'contractor_code': record.employee.contractor.contractor_code,
                'contractor_name': record.employee.contractor.contractor_name,
                'punchdate': record.punchdate.isoformat(),
                'shift': record.shift,
                'punch1_in': str(record.punch1_in) if record.punch1_in else None,
                'punch2_out': str(record.punch2_out) if record.punch2_out else None,
                'hours_worked': str(record.hours_worked) if record.hours_worked else None,
                'overstay': str(record.overstay) if record.overstay else None,
                'status': record.status
            })
        
        return JsonResponse({
            'success': True,
            'data': data,
            'page': page,
            'page_size': page_size,
            'total': total,
            'pages': (total + page_size - 1) // page_size
        })
        
    except Exception as e:
        logger.error(f"Query attendance error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def query_punch_records(request):
    """
    Query punch records with all fields
    
    GET /api/excel/punch-records/
    """
    try:
        # Get query parameters
        ep_no = request.GET.get('ep_no', '').strip()
        date_from = request.GET.get('date_from', '')
        date_to = request.GET.get('date_to', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 50))
        
        # Start with all punch records
        queryset = PunchRecord.objects.select_related('employee', 'employee__contractor')
        
        # Apply role-based filtering
        queryset = permission_service.filter_queryset(queryset, request.user)
        
        # Apply filters
        if ep_no:
            queryset = queryset.filter(employee__ep_no=ep_no)
        
        if date_from:
            queryset = queryset.filter(punchdate__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(punchdate__lte=date_to)
        
        # Get total count
        total = queryset.count()
        
        # Paginate
        start = (page - 1) * page_size
        end = start + page_size
        records = queryset[start:end]
        
        # Serialize with all fields
        data = []
        for record in records:
            data.append({
                'id': record.id,
                'ep_no': record.employee.ep_no,
                'ep_name': record.employee.ep_name,
                'punchdate': record.punchdate.isoformat(),
                'shift': record.shift,
                'punch1_in': str(record.punch1_in) if record.punch1_in else None,
                'punch2_out': str(record.punch2_out) if record.punch2_out else None,
                'punch3_in': str(record.punch3_in) if record.punch3_in else None,
                'punch4_out': str(record.punch4_out) if record.punch4_out else None,
                'punch5_in': str(record.punch5_in) if record.punch5_in else None,
                'punch6_out': str(record.punch6_out) if record.punch6_out else None,
                'early_in': str(record.early_in) if record.early_in else None,
                'late_come': str(record.late_come) if record.late_come else None,
                'early_out': str(record.early_out) if record.early_out else None,
                'hours_worked': str(record.hours_worked) if record.hours_worked else None,
                'overstay': str(record.overstay) if record.overstay else None,
                'overtime': str(record.overtime) if record.overtime else None,
                'status': record.status,
                'regular_hours': str(record.regular_hours) if record.regular_hours else None,
                'manual_request': record.manual_request
            })
        
        return JsonResponse({
            'success': True,
            'data': data,
            'page': page,
            'page_size': page_size,
            'total': total
        })
        
    except Exception as e:
        logger.error(f"Query punch records error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def query_requests(request):
    """
    Query overtime, partial day, and regularization requests
    
    GET /api/excel/requests/
    Query params: ep_no, status, request_type, date_from, date_to
    """
    try:
        # Get query parameters
        ep_no = request.GET.get('ep_no', '').strip()
        status = request.GET.get('status', '')
        request_type = request.GET.get('request_type', 'all')  # all, overtime, partial_day, regularization
        date_from = request.GET.get('date_from', '')
        date_to = request.GET.get('date_to', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 50))
        
        results = {
            'overtime': [],
            'partial_day': [],
            'regularization': []
        }
        
        # Query overtime requests
        if request_type in ['all', 'overtime']:
            ot_queryset = OvertimeRequest.objects.select_related('employee')
            ot_queryset = permission_service.filter_queryset(ot_queryset, request.user)
            
            if ep_no:
                ot_queryset = ot_queryset.filter(employee__ep_no=ep_no)
            if status:
                ot_queryset = ot_queryset.filter(status=status)
            if date_from:
                ot_queryset = ot_queryset.filter(punchdate__gte=date_from)
            if date_to:
                ot_queryset = ot_queryset.filter(punchdate__lte=date_to)
            
            for req in ot_queryset[:page_size]:
                results['overtime'].append({
                    'id': req.id,
                    'ep_no': req.employee.ep_no,
                    'ep_name': req.employee.ep_name,
                    'punchdate': req.punchdate.isoformat(),
                    'actual_overstay': str(req.actual_overstay) if req.actual_overstay else None,
                    'requested_overtime': str(req.requested_overtime) if req.requested_overtime else None,
                    'approved_overtime': str(req.approved_overtime) if req.approved_overtime else None,
                    'status': req.status
                })
        
        # Query partial day requests
        if request_type in ['all', 'partial_day']:
            pd_queryset = PartialDayRequest.objects.select_related('employee')
            pd_queryset = permission_service.filter_queryset(pd_queryset, request.user)
            
            if ep_no:
                pd_queryset = pd_queryset.filter(employee__ep_no=ep_no)
            if status:
                pd_queryset = pd_queryset.filter(status=status)
            if date_from:
                pd_queryset = pd_queryset.filter(punchdate__gte=date_from)
            if date_to:
                pd_queryset = pd_queryset.filter(punchdate__lte=date_to)
            
            for req in pd_queryset[:page_size]:
                results['partial_day'].append({
                    'id': req.id,
                    'ep_no': req.employee.ep_no,
                    'ep_name': req.employee.ep_name,
                    'punchdate': req.punchdate.isoformat(),
                    'actual_pd_hours': str(req.actual_pd_hours) if req.actual_pd_hours else None,
                    'requested_pd_hours': str(req.requested_pd_hours) if req.requested_pd_hours else None,
                    'approved_pd_hours': str(req.approved_pd_hours) if req.approved_pd_hours else None,
                    'manday_conversion': float(req.manday_conversion),
                    'status': req.status
                })
        
        # Query regularization requests
        if request_type in ['all', 'regularization']:
            reg_queryset = RegularizationRequest.objects.select_related('employee')
            reg_queryset = permission_service.filter_queryset(reg_queryset, request.user)
            
            if ep_no:
                reg_queryset = reg_queryset.filter(employee__ep_no=ep_no)
            if status:
                reg_queryset = reg_queryset.filter(status=status)
            if date_from:
                reg_queryset = reg_queryset.filter(punchdate__gte=date_from)
            if date_to:
                reg_queryset = reg_queryset.filter(punchdate__lte=date_to)
            
            for req in reg_queryset[:page_size]:
                results['regularization'].append({
                    'id': req.id,
                    'ep_no': req.employee.ep_no,
                    'ep_name': req.employee.ep_name,
                    'punchdate': req.punchdate.isoformat(),
                    'old_punch_in': str(req.old_punch_in) if req.old_punch_in else None,
                    'old_punch_out': str(req.old_punch_out) if req.old_punch_out else None,
                    'new_punch_in': str(req.new_punch_in) if req.new_punch_in else None,
                    'new_punch_out': str(req.new_punch_out) if req.new_punch_out else None,
                    'status': req.status
                })
        
        return JsonResponse({
            'success': True,
            'data': results
        })
        
    except Exception as e:
        logger.error(f"Query requests error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def dashboard_data(request):
    """
    Get dashboard data for current user
    
    GET /api/excel/dashboard/
    """
    try:
        # Get date range (default to current month)
        today = datetime.now().date()
        first_day = today.replace(day=1)
        date_from = request.GET.get('date_from', first_day.isoformat())
        date_to = request.GET.get('date_to', today.isoformat())
        
        # Get punch records with role-based filtering
        queryset = PunchRecord.objects.select_related('employee')
        queryset = permission_service.filter_queryset(queryset, request.user)
        queryset = queryset.filter(punchdate__gte=date_from, punchdate__lte=date_to)
        
        # Calculate summary statistics
        total_records = queryset.count()
        present_count = queryset.filter(status='P').count()
        absent_count = queryset.filter(status='A').count()
        
        # Get unique employees
        unique_employees = queryset.values('employee__ep_no').distinct().count()
        
        # Get recent records
        recent_records = queryset.order_by('-punchdate')[:10]
        recent_data = []
        for record in recent_records:
            recent_data.append({
                'ep_no': record.employee.ep_no,
                'ep_name': record.employee.ep_name,
                'punchdate': record.punchdate.isoformat(),
                'status': record.status,
                'hours_worked': str(record.hours_worked) if record.hours_worked else None
            })
        
        # Get pending requests count
        pending_overtime = OvertimeRequest.objects.filter(status='Pending')
        pending_overtime = permission_service.filter_queryset(pending_overtime, request.user).count()
        
        pending_partial_day = PartialDayRequest.objects.filter(status='Pending')
        pending_partial_day = permission_service.filter_queryset(pending_partial_day, request.user).count()
        
        pending_regularization = RegularizationRequest.objects.filter(status='Pending')
        pending_regularization = permission_service.filter_queryset(pending_regularization, request.user).count()
        
        return JsonResponse({
            'success': True,
            'summary': {
                'total_records': total_records,
                'present_count': present_count,
                'absent_count': absent_count,
                'unique_employees': unique_employees,
                'pending_requests': {
                    'overtime': pending_overtime,
                    'partial_day': pending_partial_day,
                    'regularization': pending_regularization
                }
            },
            'recent_records': recent_data,
            'date_range': {
                'from': date_from,
                'to': date_to
            }
        })
        
    except Exception as e:
        logger.error(f"Dashboard data error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
