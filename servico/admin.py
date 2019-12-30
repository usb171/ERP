from django.contrib import admin
from servico.models import Servico


class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'valor_total', 'tempo', 'ativo']

admin.site.register(Servico, ServicoAdmin)
