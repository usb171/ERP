from django.contrib import admin
from .models import Conta

class contaAdmin(admin.ModelAdmin):
    list_display = ['nomeCompleto', 'user', 'email', 'ativo']
    search_fields = ['user', 'nomeCompleto', 'email']
    list_filter = ['ativo']

admin.site.register(Conta, contaAdmin)
