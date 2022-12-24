from django import template

register = template.Library()

@register.filter(name='filter_range')
def filter_range(value):
    """Removes all values of arg from the given string"""
    return value[:200] + '...'