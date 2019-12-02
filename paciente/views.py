from django.shortcuts import render
from django.http import JsonResponse
from .models import Paciente
from .forms import PacienteForm
from django.contrib.auth.decorators import login_required
from .funcoes.paciente import listarTabela, getColunasTabelaHtml


class Paciente_Ajax():

    @login_required(login_url='login')
    def getDados(request):
        try:
            id = request.GET.get("id")
            paciente = Paciente.objects.get(id=id)
            contexto = {'nomeCompleto': paciente.nomeCompleto,
                        'whatsapp': paciente.whatsapp,
                        'telefone': paciente.telefone,
                        'cidade': paciente.cidade,
                        'cep': paciente.cep,
                        'facebook': paciente.facebook,
                        'instagram': paciente.instagram,
                        'email': paciente.email,
                        }

            return JsonResponse({'paciente': contexto})
        except:
            return JsonResponse({'paciente': 'Não foi possível encontrar dados do paciente de id: ' + id})


class PacienteView():

    @login_required(login_url='login')
    def paciente(request):
        template_name = "paciente/paginas/paciente.html"
        context = {'pacientes': [], 'colunas': getColunasTabelaHtml()}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return JsonResponse(PacienteForm().criarEditarExcluir(request))

    @login_required(login_url='login')
    def buscarPacientes(request):
        return JsonResponse(listarTabela(request))