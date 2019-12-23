from django import template
from django.conf import settings
from ..models import CARGO

register = template.Library()


@register.simple_tag
def get_setting(name):
    return getattr(settings, name, "")


@register.simple_tag
def get_dados_empresa(name):
    return getattr(settings, '_DADOS_PROJETO_', '')[name]


@register.simple_tag
def get_nome_cargo(cod):
    return list(filter(lambda c: c[0] == cod, CARGO))[0][1]
