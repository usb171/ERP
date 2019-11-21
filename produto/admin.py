from django.contrib import admin

from produto.models import Produto


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome_produto', 'valor_produto']

admin.site.register(Produto, ProdutoAdmin)
