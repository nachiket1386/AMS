from django import template

register = template.Library()

@register.filter(name='shift_code')
def shift_code(value):
    """
    Extract shift code from shift string.
    Example: 'CPP6 (20:00-04:00)' or 'G(09:00-17:30)' -> 'CPP6' or 'G'
    """
    if not value:
        return value
    
    # Split by opening parenthesis and take the first part
    if '(' in value:
        return value.split('(')[0].strip()
    
    return value
