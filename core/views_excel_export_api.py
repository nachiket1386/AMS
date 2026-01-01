"""
Export API Views for Excel File Upload Integration

This module provides REST API endpoints for exporting attendance data.
"""
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import pandas as pd
import json
import logging

from core.models import PunchRecord, DailySummary, OvertimeRequest, PartialDayRequest, RegularizationRequest
from core.services.permission_service import PermissionService
from core.services.export_service import ExportService

logger = logging.getLogger(__name__)

# Initialize services
permission_service = PermissionService()
export_service = ExportService()


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def export_data(request):
    """
    Export filtered data to CSV
    
    POST /api/excel/export/
    Body: {
        "data_type": "punch_records|daily_summary|overtime|partial_day|regularization",
        "filters": {
            "ep_no": "...",
            "date_from": "...",
            "date_to": "...",
            "status": "..."
        },
        "format": "csv|excel"
    }
    """
    try:
        # Parse request body
        data = json.loads(request.body)
        data_type = data.get('data_type', 'punch_records')
        filters = data.get('filters', {})
        export_format = data.get('format', 'csv')
        
        # Get queryset based on data type
        if data_type == 'punch_records':
            queryset = PunchRecord.objects.select_related('employee', 'employee__contractor')
        elif data_type == 'daily_summary':
            queryset = DailySummary.objects.select_related('employee')
        elif data_type == 'overtime':
            queryset = OvertimeRequest.objects.select_related('employee')
        elif data_type == 'partial_day':
            queryset = PartialDayRequest.objects.select_related('employee')
        elif data_type == 'regularization':
            queryset = RegularizationRequest.objects.select_related('employee')
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid data type'
            }, status=400)
        
        # Apply role-based filtering
        queryset = permission_service.filter_queryset(queryset, request.user)
        
        # Apply filters
        ep_no = filters.get('ep_no', '').strip()
        if ep_no:
            queryset = queryset.filter(employee__ep_no__icontains=ep_no)
        
        date_from = filters.get('date_from', '')
        if date_from:
            queryset = queryset.filter(punchdate__gte=date_from)
        
        date_to = filters.get('date_to', '')
        if date_to:
            queryset = queryset.filter(punchdate__lte=date_to)
        
        status = filters.get('status', '')
        if status and hasattr(queryset.model, 'status'):
            queryset = queryset.filter(status=status)
        
        # Check if queryset is empty
        record_count = queryset.count()
        if record_count == 0:
            return JsonResponse({
                'success': False,
                'error': 'No records found matching the filters'
            }, status=404)
        
        # Check export size limit (max 100K records)
        if record_count > 100000:
            return JsonResponse({
                'success': False,
                'error': f'Export size ({record_count} records) exceeds limit of 100,000. Please apply more filters.'
            }, status=400)
        
        # Convert queryset to DataFrame
        data_list = []
        for record in queryset:
            row = {
                'EP_NO': record.employee.ep_no,
                'EP_NAME': record.employee.ep_name,
                'CONTRACTOR_CODE': record.employee.contractor.contractor_code,
                'CONTRACTOR_NAME': record.employee.contractor.contractor_name,
                'PUNCHDATE': record.punchdate.isoformat(),
            }
            
            # Add type-specific fields
            if data_type == 'punch_records':
                row.update({
                    'SHIFT': record.shift,
                    'PUNCH1_IN': str(record.punch1_in) if record.punch1_in else '',
                    'PUNCH2_OUT': str(record.punch2_out) if record.punch2_out else '',
                    'HOURS_WORKED': str(record.hours_worked) if record.hours_worked else '',
                    'OVERSTAY': str(record.overstay) if record.overstay else '',
                    'STATUS': record.status
                })
            elif data_type == 'daily_summary':
                row.update({
                    'MANDAYS': float(record.mandays),
                    'REGULAR_MANDAY_HR': str(record.regular_manday_hr) if record.regular_manday_hr else '',
                    'OT': float(record.ot)
                })
            elif data_type == 'overtime':
                row.update({
                    'ACTUAL_OVERSTAY': str(record.actual_overstay) if record.actual_overstay else '',
                    'REQUESTED_OVERTIME': str(record.requested_overtime) if record.requested_overtime else '',
                    'APPROVED_OVERTIME': str(record.approved_overtime) if record.approved_overtime else '',
                    'STATUS': record.status
                })
            elif data_type == 'partial_day':
                row.update({
                    'ACTUAL_PD_HOURS': str(record.actual_pd_hours) if record.actual_pd_hours else '',
                    'REQUESTED_PD_HOURS': str(record.requested_pd_hours) if record.requested_pd_hours else '',
                    'APPROVED_PD_HOURS': str(record.approved_pd_hours) if record.approved_pd_hours else '',
                    'MANDAY_CONVERSION': float(record.manday_conversion),
                    'STATUS': record.status
                })
            elif data_type == 'regularization':
                row.update({
                    'OLD_PUNCH_IN': str(record.old_punch_in) if record.old_punch_in else '',
                    'OLD_PUNCH_OUT': str(record.old_punch_out) if record.old_punch_out else '',
                    'NEW_PUNCH_IN': str(record.new_punch_in) if record.new_punch_in else '',
                    'NEW_PUNCH_OUT': str(record.new_punch_out) if record.new_punch_out else '',
                    'STATUS': record.status
                })
            
            data_list.append(row)
        
        df = pd.DataFrame(data_list)
        
        # Generate filename
        filename = export_service.generate_filename(data_type, request.user)
        
        # Log export
        export_service.log_export(
            user=request.user,
            export_type=data_type,
            record_count=record_count,
            filters=filters
        )
        
        # Generate response based on format
        if export_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            df.to_csv(response, index=False)
        elif export_format == 'excel':
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            filename = filename.replace('.csv', '.xlsx')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            df.to_excel(response, index=False, engine='openpyxl')
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid export format'
            }, status=400)
        
        logger.info(f"Exported {record_count} {data_type} records for {request.user.username}")
        return response
        
    except Exception as e:
        logger.error(f"Export error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def export_logs(request):
    """
    Get export logs for current user
    
    GET /api/excel/export/logs/
    """
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        
        # Filter by user role
        from core.models import ExportLog
        if request.user.role == 'root':
            logs = ExportLog.objects.all()
        else:
            logs = ExportLog.objects.filter(user=request.user)
        
        # Paginate
        start = (page - 1) * page_size
        end = start + page_size
        total = logs.count()
        logs = logs[start:end]
        
        # Serialize
        data = []
        for log in logs:
            data.append({
                'id': log.id,
                'export_type': log.export_type,
                'record_count': log.record_count,
                'filters': log.filters,
                'created_at': log.created_at.isoformat(),
                'user': log.user.username if log.user else 'Unknown'
            })
        
        return JsonResponse({
            'success': True,
            'data': data,
            'page': page,
            'page_size': page_size,
            'total': total
        })
        
    except Exception as e:
        logger.error(f"Export logs error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
