from django import template

register = template.Library()


@register.filter
def star_rating(rating):
    """
    Convert a numeric rating (0-10) to a 5-star display (★☆).
    Returns a string with filled stars (★), half stars (½), and empty stars (☆).
    """
    if not rating or rating < 0:
        return '☆☆☆☆☆'
    
    # Convert 0-10 scale to 0-5 scale
    stars = rating / 2
    
    result = ''
    for i in range(1, 6):
        if i <= stars:
            result += '★'
        elif i - 0.5 == stars:
            result += '½'
        else:
            result += '☆'
    
    return result


@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, arg):
    """Divide the value by the argument"""
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def format_join_date(date_obj):
    """
    Format join date in Ukrainian style.
    Example: 2024-05-15 -> "Читач з травня 2024"
    """
    if not date_obj:
        return ''
    
    months = {
        1: 'січня',
        2: 'лютого',
        3: 'березня',
        4: 'квітня',
        5: 'травня',
        6: 'червня',
        7: 'липня',
        8: 'серпня',
        9: 'вересня',
        10: 'жовтня',
        11: 'листопада',
        12: 'грудня',
    }
    
    month_name = months.get(date_obj.month, '')
    year = date_obj.year
    
    return f'Читач з {month_name} {year}'
