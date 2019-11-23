from django import forms
from .funcoes.produto import criarEditarExcluir


class ProdutoForm(forms.Form):

    def criarEditarExcluir(self, request):
        super(ProdutoForm, self).is_valid()
        return criarEditarExcluir(request)
