from django.shortcuts import render
from django.http import JsonResponse
from .forms import PacienteForm
from django.contrib.auth.decorators import login_required
from .funcoes.paciente import getPacientesString, getPaciente as getPacienteF, getPacientes as getPacientesF


class PacienteAjax():
    @login_required(login_url='login')
    def getPaciente(request):
        return JsonResponse(getPacienteF(request))

    @login_required(login_url='login')
    def getPacientes(request):
        return JsonResponse(getPacientesF(request))


class PacienteView():
    @login_required(login_url='login')
    def paciente(request):
        template_name = "paciente/paginas/paciente.html"
        context = {'pacientes': getPacientesString()}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return JsonResponse(PacienteForm().criarEditarExcluir(request))
