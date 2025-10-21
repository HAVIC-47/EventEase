from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies the value by the argument."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add_class(field, css_class):
    """Adds CSS class to form field."""
    return field.as_widget(attrs={"class": css_class})

@register.filter
def range_filter(value):
    """Returns a range from 0 to value."""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)