from django import forms
from .funcoes.financeiro import criarEditarExcluir
from .funcoes.Despesa import criarEditarExcluirD

class ReceitaForm(forms.Form):
    def criarEditarExcluir(self, request):
        super(ReceitaForm, self).is_valid()
        return criarEditarExcluir(request)

class DespesaForm(forms.Form):
    def criarEditarExcluir(self, request):
        super(DespesaForm, self).is_valid()
        return criarEditarExcluirD(request)