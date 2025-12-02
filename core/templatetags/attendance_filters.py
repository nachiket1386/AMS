"""
Custom template filters for attendance display
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def format_time_pairs(record):
    """
    Format IN/OUT time pairs as "IN → OUT" format with color coordination
    IN times: Red color (arrival/entry)
    OUT times: Green color (departure/exit)
    Example: "09:00 → 17:00 | 09:15 → 12:00"
    """
    pairs = []
    
    # First pair (IN/OUT)
    if record.in_time or record.out_time:
        in_time = record.in_time.strftime('%H:%M') if record.in_time else '--:--'
        out_time = record.out_time.strftime('%H:%M') if record.out_time else '--:--'
        pairs.append(f'<span style="color: #dc2626; font-weight: 600;">{in_time}</span> → <span style="color: #16a34a; font-weight: 600;">{out_time}</span>')
    
    # Second pair (IN(2)/OUT(2))
    if record.in_time_2 or record.out_time_2:
        in_time_2 = record.in_time_2.strftime('%H:%M') if record.in_time_2 else '--:--'
        out_time_2 = record.out_time_2.strftime('%H:%M') if record.out_time_2 else '--:--'
        pairs.append(f'<span style="color: #dc2626; font-weight: 600;">{in_time_2}</span> → <span style="color: #16a34a; font-weight: 600;">{out_time_2}</span>')
    
    # Third pair (IN(3)/OUT(3))
    if record.in_time_3 or record.out_time_3:
        in_time_3 = record.in_time_3.strftime('%H:%M') if record.in_time_3 else '--:--'
        out_time_3 = record.out_time_3.strftime('%H:%M') if record.out_time_3 else '--:--'
        pairs.append(f'<span style="color: #dc2626; font-weight: 600;">{in_time_3}</span> → <span style="color: #16a34a; font-weight: 600;">{out_time_3}</span>')
    
    result = ' <span style="color: #666;">|</span> '.join(pairs) if pairs else '-'
    return mark_safe(result)


@register.filter
def has_excessive_overstay(overstay_str):
    """
    Check if overstay exceeds 01:00 hours
    Returns True if overstay > 01:00, False otherwise
    """
    if not overstay_str or overstay_str == '-':
        return False
    
    try:
        # Parse overstay string (format: HH:MM)
        parts = str(overstay_str).split(':')
        if len(parts) == 2:
            hours = int(parts[0])
            minutes = int(parts[1])
            total_minutes = hours * 60 + minutes
            return total_minutes > 60  # More than 01:00
    except (ValueError, AttributeError):
        pass
    
    return False


@register.filter
def format_overstay(overstay_str):
    """
    Format overstay value with bold red text if > 01:00
    """
    if not overstay_str or overstay_str == '-':
        return mark_safe('-')
    
    if has_excessive_overstay(overstay_str):
        return mark_safe(f'<span style="color: #dc2626; font-weight: 700;">{overstay_str}</span>')
    else:
        return overstay_str
