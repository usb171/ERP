from django import forms
from .funcoes.servico import criarEditarExcluir

class ServicoForm(forms.Form):
    def criarEditarExcluir(self, request):
        super(ServicoForm, self).is_valid()
        return criarEditarExcluir(request)