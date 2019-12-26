from django.contrib import admin
from servico.models import Servico


class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome_servico', 'valor_servico', 'tempo_servico']

admin.site.register(Servico, ServicoAdmin)
