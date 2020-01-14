from django.contrib import admin
from financeiro.models import Despesa, Categoria, Receita


class DespesaAdim(admin.ModelAdmin):
    list_display = ['descricao', 'categoria', 'data_vencimento', 'valor', 'data_pagamento']


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'observacao']


class ReceitaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'valor_apagar', 'forma_pagamento']


admin.site.register(Despesa, DespesaAdim)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Receita, ReceitaAdmin)