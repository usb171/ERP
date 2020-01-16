from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .funcoes.agenda import buscarDisponibilidade as buscarDisponibilidadeF,\
                            get_options_periodos,\
                            initTimepickerHorario,\
                            agendar as agendarF,\
                            carregarAgenda as carregarAgendaF


class AgendaView():

    @login_required(login_url='login')
    def agenda(request):
        template_name = "agenda/paginas/agenda2.html"
        context = {'agenda': [],
                   'options_periodos': get_options_periodos(),
                   'timepickerHorario': initTimepickerHorario()
                   }
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return None


class AgendaAjax():

    @login_required(login_url='login')
    def carregarAgenda(request):
        return JsonResponse(carregarAgendaF(request))

    @login_required(login_url='login')
    def buscarDisponibilidade(request):
        return JsonResponse(buscarDisponibilidadeF(request))

    @login_required(login_url='login')
    def agendar(request):
        return JsonResponse(agendarF(request))
