import os
from django import template

register = template.Library()

@register.filter
def file_exists(path):
    return os.path.exists(path)