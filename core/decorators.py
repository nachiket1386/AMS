"""
Permission decorators for role-based access control
"""
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
import logging

logger = logging.getLogger('core')


def role_required(allowed_roles):
    """
    Decorator to restrict access based on user role.
    
    Args:
        allowed_roles: List of allowed role strings (e.g., ['root', 'admin'])
    
    Usage:
        @role_required(['root', 'admin'])
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                logger.warning(
                    f'Permission denied: User {request.user.username} (role: {request.user.role}) '
                    f'attempted to access {view_func.__name__} (requires: {allowed_roles})'
                )
                messages.error(request, 'You do not have permission to access this page.')
                return HttpResponseForbidden('Access Denied: Insufficient permissions')
        return wrapper
    return decorator


def company_access_required(view_func):
    """
    Decorator to ensure users can only access their company data.
    This should be used in conjunction with queryset filtering in views.
    
    Usage:
        @company_access_required
        def my_view(request):
            ...
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        # Root users have access to all companies
        if request.user.role == 'root':
            return view_func(request, *args, **kwargs)
        
        # Admin and User1 must have a company assigned
        if not request.user.company:
            messages.error(request, 'Your account is not associated with a company.')
            return redirect('core:dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def check_record_company_access(user, record):
    """
    Helper function to check if user has access to a specific record's company.
    
    Args:
        user: User object
        record: Record object with a 'company' attribute
    
    Returns:
        Boolean indicating if user has access
    """
    if user.role == 'root':
        return True
    
    if user.company and record.company == user.company:
        return True
    
    return False


def can_edit_record(user):
    """
    Helper function to check if user can edit records.
    
    Args:
        user: User object
    
    Returns:
        Boolean indicating if user can edit
    """
    return user.role in ['root', 'admin']


def can_delete_record(user):
    """
    Helper function to check if user can delete records.
    
    Args:
        user: User object
    
    Returns:
        Boolean indicating if user can delete
    """
    return user.role in ['root', 'admin']


def can_upload_csv(user):
    """
    Helper function to check if user can upload CSV files.
    
    Args:
        user: User object
    
    Returns:
        Boolean indicating if user can upload
    """
    return user.role in ['root', 'admin']


def can_manage_users(user):
    """
    Helper function to check if user can manage other users.
    
    Args:
        user: User object
    
    Returns:
        Boolean indicating if user can manage users
    """
    return user.role in ['root', 'admin']
