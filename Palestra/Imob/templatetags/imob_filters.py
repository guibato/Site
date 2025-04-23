import os
from django import template

register = template.Library()

@register.filter
def file_exists(path):
    return os.path.exists(path)

def replace(value, arg):
    """
    Substitui um caractere por outro em uma string.
    Uso: {{ valor|replace:"antigo,novo" }}
    """
    if not value:
        return value
    try:
        old, new = arg.split(',')
        return value.replace(old, new)
    except ValueError:
        # Caso os argumentos não estejam no formato correto
        return value