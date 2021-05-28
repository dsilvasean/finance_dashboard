from atexit import register
from django import template

register = template.Library()

@register.filter()
def to_int(value):
    value_ = int(value)
    return value_

@register.filter()
def to_float(value):
    value_ = float(value)
    return value_