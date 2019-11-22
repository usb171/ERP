from django import forms
from .models import *
from .funcoes.paciente import criarEditarExcluir

class PacienteForm(forms.Form):

    def criarEditarExcluir(self, request):
        super(PacienteForm, self).is_valid()
        return criarEditarExcluir(request)

class CadastroPacienteForm(forms.Form):
    nome = forms.CharField(required=True)
    telefone = forms.CharField(required=True)
    cidade = forms.CharField(required=True)
    estado = forms.CharField(required=True)
    rede_social = forms.CharField(required=True)

    def save(self):
        if self.is_valid():
            status = {'form': self.cleaned_data}
            paciente = Paciente.objects.create(**self.cleaned_data)
            paciente.save()
            return status

    def editar(self, paciente):
        if self.is_valid():
            status = {'form': self.cleaned_data}
            paciente = Paciente.objects.get(pk=paciente.id)
            paciente.nome = self.cleaned_data['nome']
            paciente.telefone = self.cleaned_data['telefone']
            paciente.cidade = self.cleaned_data['cidade']
            paciente.estado = self.cleaned_data['estado']
            paciente.rede_social = self.cleaned_data['rede_social']

            paciente.save()
            return status
        else:
            status = {'form': self.cleaned_data}
            return status

    def getForm(self, paciente):
        return {'form': Paciente.objects.filter(pk=paciente.id).values()[0]}

    def is_valid(self):
        super(CadastroPacienteForm, self).is_valid()
        return True
