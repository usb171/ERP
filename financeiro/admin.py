from django.contrib import admin
from financeiro.models import Despesa, Categoria


class DespesaAdim(admin.ModelAdmin):
    list_display = ['descricao', 'categoria', 'data_vencimento', 'valor', 'data_pagamento']



class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'observacao']




admin.site.register(Despesa, DespesaAdim)
admin.site.register(Categoria, CategoriaAdmin)