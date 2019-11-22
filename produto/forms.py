from django import forms
from .funcoes.produto import Produto


class ProdutoForm(forms.Form):

    def criarOuEditar(self, request):
        super(ProdutoForm, self).is_valid()
        return Produto.criarOuEditar(request)
