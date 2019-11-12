from django import forms
from .funcoes.sessao import Sessao
class FormConta(forms.Form):

    """
    * Class FormConta
    """

    email = forms.CharField(required=True)
    senha = forms.CharField(required=True)

    def login(self, request):
        super(FormConta, self).is_valid()
        email = self.cleaned_data['email']
        senha = self.cleaned_data['senha']
        return Sessao.login(email, senha, request)

