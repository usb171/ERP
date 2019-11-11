from django.shortcuts import render, redirect
from .forms import *

class Cadastro():
    def pacienteView(request):
        template_name = 'paciente/cadastro_paciente.html'
        contexto = {'nome': Paciente.nome,
                    'telefone': Paciente.telefone,
                    'cidade': Paciente.cidade,
                    'estado': Paciente.estado,
                    'rede_social': Paciente.rede_social}

        if request.method == 'GET':
            return render(request, template_name, contexto)
        elif request.method == 'POST':
            form = CadastroPacienteForm(request.POST).save(request)
            return redirect('index')