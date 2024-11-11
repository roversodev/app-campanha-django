from django import template

register = template.Library()  # This line registers the filter library

@register.filter
def split(value):
    """Dividir a string por espaços"""
    return value.split()

@register.filter
def capitalize_words(value):
    """Capitaliza a primeira letra de cada palavra e transforma o resto em minúsculas"""
    return ' '.join(word.capitalize() for word in value.split())

@register.filter
def truncate_text(value, arg):
    """Trunca o texto para o número de caracteres especificado."""
    if isinstance(value, str) and len(value) > arg:
        return value[:arg] + '...'  # Adiciona '...' se o texto for maior que o limite
    return value  # Retorna o texto original se não for maior que o limite


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])
