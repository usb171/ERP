from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_setting(name):
    return getattr(settings, name, "")

@register.simple_tag
def get_dados_empresa(name):
    return getattr(settings, '_DADOS_PROJETO_', '')[name]