from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Paciente
from .forms import CadastroPacienteForm, PacienteForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required


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
        context = {'pacientes': []}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return JsonResponse(PacienteForm().criarOuEditar(request))

    @login_required(login_url='login')
    def buscarPacientes(request):

        busca = request.GET.get('search[value]')
        pacientes_total = Paciente.objects.all()
        pacientes_filtro = Paciente.objects.filter(
            (Q(nomeCompleto__contains=busca) | Q(email__contains=busca))).order_by('nomeCompleto')\
            .values('id', 'nomeCompleto', 'whatsapp', 'telefone', 'email')

        pacientes_filtro = list(map(lambda paciente: list(paciente.values()), pacientes_filtro))

        context = {"recordsTotal": len(pacientes_total),
                   "recordsFiltered": len(pacientes_filtro),
                   "data": pacientes_filtro
                   }
        return JsonResponse(context)
