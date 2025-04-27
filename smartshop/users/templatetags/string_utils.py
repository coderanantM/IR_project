# users/templatetags/string_utils.py
from django import template

register = template.Library()

@register.filter(name='split')
def split_string(value, key=','):
    """
    Splits a string by the specified delimiter.
    Usage: {{ some_string|split:"," }}
    """
    if value is None:
        return []
    return str(value).split(key)

