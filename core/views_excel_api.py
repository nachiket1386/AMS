"""
API Views for Excel File Upload Integration

This module provides REST API endpoints for Excel file upload, validation, and import.
"""
import os
import json
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.conf import settings
import pandas as pd
import logging

from core.models import ImportLog, ExportLog, UploadPermission, User
from core.services.file_parser_service import FileParserService, FileType
from core.services.data_validator_service import DataValidatorService
from core.services.data_importer_service import DataImporterService
from core.services.permission_service import PermissionService

logger = logging.getLogger(__name__)

# Initialize services
file_parser = FileParserService()
validator = DataValidatorService()
importer = DataImporterService()
permission_service = PermissionService()


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def upload_excel_file(request):
    """
    Upload Excel file and return session ID
    
    POST /api/excel/upload/
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'No file uploaded'
            }, status=400)
        
        uploaded_file = request.FILES['file']
        
        # Validate file extension
        if not uploaded_file.name.endswith(('.xls', '.xlsx')):
            return JsonResponse({
                'success': False,
                'error': 'Only .xls and .xlsx files are supported'
            }, status=400)
        
        # Validate file size (max 50MB)
        max_size = 50 * 1024 * 1024  # 50MB
        if uploaded_file.size > max_size:
            return JsonResponse({
                'success': False,
                'error': f'File size exceeds maximum limit of 50MB'
            }, status=400)
        
        # Save file temporarily
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'excel_uploads', str(request.user.id))
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        logger.info(f"File uploaded: {uploaded_file.name} by {request.user.username}")
        
        return JsonResponse({
            'success': True,
            'session_id': os.path.basename(file_path),
            'filename': uploaded_file.name,
            'size': uploaded_file.size
        })
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def process_excel_file(request, session_id):
    """
    Process uploaded file: parse, detect type, validate, and AUTO-IMPORT
    
    POST /api/excel/upload/<session_id>/process/
    """
    try:
        # Get file path
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'excel_uploads', str(request.user.id))
        file_path = os.path.join(upload_dir, session_id)
        
        if not os.path.exists(file_path):
            return JsonResponse({
                'success': False,
                'error': 'File not found'
            }, status=404)
        
        # Parse file
        df, error = file_parser.parse_file(file_path)
        if error:
            return JsonResponse({
                'success': False,
                'error': error
            }, status=400)
        
        # Detect file type
        file_type = file_parser.detect_file_type(df)
        if file_type == FileType.UNKNOWN:
            return JsonResponse({
                'success': False,
                'error': 'Could not detect file type. Please ensure the file has the correct column structure.'
            }, status=400)
        
        # Check upload permission
        if not permission_service.can_upload(request.user, file_type):
            return JsonResponse({
                'success': False,
                'error': f'You do not have permission to upload {file_type.value} files'
            }, status=403)
        
        # Normalize data
        df = file_parser.normalize_data(df, file_type)
        
        # Validate data
        validation_report = validator.validate_batch(df, file_type.value)
        
        # Get preview data
        preview_df = file_parser.get_preview_data(df, 10)
        
        logger.info(f"File processed: {session_id}, type: {file_type.value}, valid: {validation_report.valid_rows}/{validation_report.total_rows}")
        
        # AUTO-IMPORT: Import data immediately after validation
        result = importer.import_batch(
            df=df,
            file_type=file_type,
            user=request.user,
            filename=session_id,
            session_id=session_id  # Pass session_id for progress tracking
        )
        
        # Clean up temporary files
        try:
            os.remove(file_path)
        except:
            pass
        
        logger.info(f"Auto-import completed: {result.imported_rows} imported, {result.duplicate_rows} duplicates")
        
        return JsonResponse({
            'success': True,
            'file_type': file_type.value,
            'total_rows': validation_report.total_rows,
            'valid_rows': validation_report.valid_rows,
            'invalid_rows': validation_report.invalid_rows,
            'duplicate_rows': len(validation_report.duplicates),
            'preview_data': preview_df.to_dict('records'),
            'preview_columns': list(preview_df.columns),
            'validation_errors': validation_report.to_dict()['errors'][:100],  # Limit to first 100 errors
            'has_errors': validation_report.invalid_rows > 0,
            # Import results
            'imported_rows': result.imported_rows,
            'import_duplicate_rows': result.duplicate_rows,
            'import_error_rows': result.error_rows,
            'import_success': result.success,
            'import_log_id': result.import_log_id,
            'import_error_message': result.error_message
        })
        
    except Exception as e:
        logger.error(f"Processing error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def get_import_progress(request, session_id):
    """
    Get real-time import progress
    
    GET /api/excel/upload/<session_id>/progress/
    """
    try:
        progress = importer.get_progress(session_id)
        
        if progress:
            return JsonResponse({
                'success': True,
                'progress': progress
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No progress data found'
            }, status=404)
            
    except Exception as e:
        logger.error(f"Progress retrieval error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def confirm_excel_import(request, session_id):
    """
    Confirm import and process all valid records
    
    POST /api/excel/upload/<session_id>/confirm/
    """
    try:
        # Get processed file
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'excel_uploads', str(request.user.id))
        processed_path = os.path.join(upload_dir, session_id + '.processed.csv')
        
        if not os.path.exists(processed_path):
            return JsonResponse({
                'success': False,
                'error': 'Processed file not found. Please process the file first.'
            }, status=404)
        
        # Read processed data
        df = pd.read_csv(processed_path)
        
        # Detect file type again
        file_type = file_parser.detect_file_type(df)
        
        # Import data
        result = importer.import_batch(
            df=df,
            file_type=file_type,
            user=request.user,
            filename=session_id
        )
        
        # Clean up temporary files
        try:
            os.remove(os.path.join(upload_dir, session_id))
            os.remove(processed_path)
        except:
            pass
        
        logger.info(f"Import completed: {result.imported_rows} imported, {result.duplicate_rows} duplicates")
        
        return JsonResponse({
            'success': result.success,
            'total_rows': result.total_rows,
            'imported_rows': result.imported_rows,
            'duplicate_rows': result.duplicate_rows,
            'error_rows': result.error_rows,
            'import_log_id': result.import_log_id,
            'error_message': result.error_message
        })
        
    except Exception as e:
        logger.error(f"Import error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def download_error_report(request, session_id):
    """
    Download error report as CSV
    
    GET /api/excel/upload/<session_id>/errors/
    """
    try:
        # Get file path
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'excel_uploads', str(request.user.id))
        file_path = os.path.join(upload_dir, session_id)
        
        if not os.path.exists(file_path):
            return JsonResponse({
                'success': False,
                'error': 'File not found'
            }, status=404)
        
        # Parse and validate file
        df, error = file_parser.parse_file(file_path)
        if error:
            return JsonResponse({
                'success': False,
                'error': error
            }, status=400)
        
        file_type = file_parser.detect_file_type(df)
        df = file_parser.normalize_data(df, file_type)
        validation_report = validator.validate_batch(df, file_type.value)
        
        # Create error report CSV
        if not validation_report.errors:
            return JsonResponse({
                'success': False,
                'error': 'No errors found'
            }, status=404)
        
        # Build error report
        error_data = []
        for error in validation_report.errors:
            error_data.append({
                'Row': error.row_number,
                'Column': error.column_name,
                'Value': error.value,
                'Error': error.error_message
            })
        
        error_df = pd.DataFrame(error_data)
        
        # Generate CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="error_report_{session_id}.csv"'
        error_df.to_csv(response, index=False)
        
        return response
        
    except Exception as e:
        logger.error(f"Error report generation failed: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def import_history(request):
    """
    Get import history for current user
    
    GET /api/excel/imports/
    """
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        
        # Filter by user role
        if request.user.role == 'root':
            logs = ImportLog.objects.all()
        else:
            logs = ImportLog.objects.filter(user=request.user)
        
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
                'filename': log.filename,
                'file_type': log.file_type,
                'total_rows': log.total_rows,
                'imported_rows': log.imported_rows,
                'duplicate_rows': log.duplicate_rows,
                'error_rows': log.error_rows,
                'status': log.status,
                'created_at': log.created_at.isoformat(),
                'user': log.user.username if log.user else 'Unknown'
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
        logger.error(f"Import history error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def import_detail(request, import_id):
    """
    Get detailed information about an import
    
    GET /api/excel/imports/<import_id>/
    """
    try:
        # Get import log
        if request.user.role == 'root':
            log = ImportLog.objects.get(id=import_id)
        else:
            log = ImportLog.objects.get(id=import_id, user=request.user)
        
        # Serialize
        data = {
            'id': log.id,
            'filename': log.filename,
            'file_type': log.file_type,
            'total_rows': log.total_rows,
            'imported_rows': log.imported_rows,
            'duplicate_rows': log.duplicate_rows,
            'error_rows': log.error_rows,
            'status': log.status,
            'error_report_path': log.error_report_path,
            'created_at': log.created_at.isoformat(),
            'user': log.user.username if log.user else 'Unknown'
        }
        
        return JsonResponse({
            'success': True,
            'data': data
        })
        
    except ImportLog.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Import log not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Import detail error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET", "POST", "DELETE"])
@csrf_exempt
def manage_permissions(request):
    """
    Manage upload permissions
    
    GET /api/excel/permissions/ - List permissions
    POST /api/excel/permissions/ - Grant permission
    DELETE /api/excel/permissions/<id>/ - Revoke permission
    """
    # Only admin and root can manage permissions
    if request.user.role not in ['root', 'admin']:
        return JsonResponse({
            'success': False,
            'error': 'Permission denied'
        }, status=403)
    
    try:
        if request.method == 'GET':
            # List all permissions
            permissions = UploadPermission.objects.all()
            
            data = []
            for perm in permissions:
                data.append({
                    'id': perm.id,
                    'user': perm.user.username,
                    'file_type': perm.file_type,
                    'can_upload': perm.can_upload,
                    'granted_by': perm.granted_by.username if perm.granted_by else 'System',
                    'granted_at': perm.granted_at.isoformat()
                })
            
            return JsonResponse({
                'success': True,
                'data': data
            })
        
        elif request.method == 'POST':
            # Grant permission
            data = json.loads(request.body)
            user_id = data.get('user_id')
            file_type = data.get('file_type')
            
            if not user_id or not file_type:
                return JsonResponse({
                    'success': False,
                    'error': 'user_id and file_type are required'
                }, status=400)
            
            user = User.objects.get(id=user_id)
            permission = permission_service.grant_permission(user, file_type, request.user)
            
            return JsonResponse({
                'success': True,
                'data': {
                    'id': permission.id,
                    'user': permission.user.username,
                    'file_type': permission.file_type,
                    'can_upload': permission.can_upload
                }
            })
        
        elif request.method == 'DELETE':
            # Revoke permission
            perm_id = request.GET.get('id')
            if not perm_id:
                return JsonResponse({
                    'success': False,
                    'error': 'Permission ID is required'
                }, status=400)
            
            permission = UploadPermission.objects.get(id=perm_id)
            permission.can_upload = False
            permission.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Permission revoked'
            })
        
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'User not found'
        }, status=404)
    except UploadPermission.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Permission not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Permission management error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def upload_audit_log(request):
    """
    Get upload audit log
    
    GET /api/excel/audit/uploads/
    """
    # Only admin and root can view audit log
    if request.user.role not in ['root', 'admin']:
        return JsonResponse({
            'success': False,
            'error': 'Permission denied'
        }, status=403)
    
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 50))
        
        # Get all import logs
        logs = ImportLog.objects.all()
        
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
                'user': log.user.username if log.user else 'Unknown',
                'filename': log.filename,
                'file_type': log.file_type,
                'status': log.status,
                'total_rows': log.total_rows,
                'imported_rows': log.imported_rows,
                'created_at': log.created_at.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'data': data,
            'page': page,
            'page_size': page_size,
            'total': total
        })
        
    except Exception as e:
        logger.error(f"Audit log error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
