from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import *

class PacienteList(ListView):
    model = Paciente

class Cadastro():
    def pacienteView(request):
        template_name = 'paciente/cadastro_paciente.html'
        paciente = Paciente.objects.all()

        if request.method == 'GET':
            return render(request, template_name, {'paciente': paciente})
        elif request.method == 'POST':
            form = CadastroPacienteForm(request.POST).save(request)
            return redirect('lista_paciente')

    def editarPaciente(request):
        id = request.GET.get('id')
        print(id)
        paciente = Paciente.objects.get(pk=id)
        template_name = 'paciente/editar_paciente.html'

        if request.method == 'GET':
            form = CadastroPacienteForm(request.POST).getForm(paciente)
            # pac['form'] = form['form']
        elif request.method == 'POST':
            form = CadastroPacienteForm(request.POST, request.FILES).editar(paciente)
            # pac['form'] = form['form']
            return redirect('lista_paciente')

        return render(request, template_name)
