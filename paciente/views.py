from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import JsonResponse
import json

from .forms import *

class Lista():
    def listarPaciente(request):
        template_name = 'paciente/paciente_list.html'
        pacientes = Paciente.objects.all()

        if request.method == 'GET':
            return render(request, template_name, {'pacientes': pacientes})
        elif request.method == 'POST':
            form = CadastroPacienteForm(request.POST).save()
            return render(request, template_name, {'pacientes': pacientes})

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
        paciente = Paciente.objects.get(pk=id)
        template_name = 'paciente/paciente_list.html'
        contexto = {'nome': Paciente.nome,
                    'telefone': Paciente.telefone,
                    'cidade': Paciente.cidade,
                    'estado': Paciente.estado,
                    'rede_social': Paciente.rede_social}
        if request.method == 'GET':
            form = CadastroPacienteForm(request.POST).getForm(paciente)
            contexto['form'] = form['form']
        elif request.method == 'POST':
            form = CadastroPacienteForm(request.POST, request.FILES).editar(paciente)
            contexto['form'] = form['form']
            return redirect('lista_paciente')

        return render(request, template_name, contexto)

class Paciente_Ajax():


    def retornarDados(request):
        id = request.GET.get("id")
        paciente = Paciente.objects.get(id=id)
        contexto = {'nome': paciente.nome,
                    'telefone': paciente.telefone,
                    'cidade': paciente.cidade,
                    'estado': paciente.estado,
                    'rede_social': paciente.rede_social}


        return JsonResponse({'paciente': contexto})
