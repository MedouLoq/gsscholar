# custom_filters.py
from django import template
import base64

register = template.Library()

@register.filter
def base64_encode(value):
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')

@register.filter(name='get_value')
def get_value(dictionary, key):
    return dictionary.get(key, None)
