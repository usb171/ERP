from django.contrib import admin

from produto.models import Produto


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'valor', 'tipo', 'quantidade', 'ativo']

admin.site.register(Produto, ProdutoAdmin)
