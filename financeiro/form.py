from django import forms
from .funcoes.financeiro import criarEditarExcluir

class ReceitaForm(forms.Form):
    def criarEditarExcluir(self, request):
        super(ReceitaForm, self).is_valid()
        return criarEditarExcluir(request)