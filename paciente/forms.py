from django.forms import ModelForm
from django import forms
from .models import *

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'telefone', 'cidade', 'estado', 'rede_social']

class CadastroPacienteForm(forms.Form):
    nome = forms.CharField(required=True)
    telefone = forms.CharField(required=True)
    cidade = forms.CharField(required=True)
    estado = forms.CharField(required=True)
    rede_social = forms.CharField(required=True)

    def save(self, request):
        if self.is_valid():
            status = {'form': self.cleaned_data}
            print(self.cleaned_data)
            return status