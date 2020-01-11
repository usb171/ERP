from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .funcoes.agenda import buscarDisponibilidade as buscarDisponibilidadeF


class AgendaView():

    @login_required(login_url='login')
    def agenda(request):
        template_name = "agenda/paginas/agenda.html"
        context = {'agenda': []}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return None


class AgendaAjax():
    @login_required(login_url='login')
    def buscarDisponibilidade(request):
        return JsonResponse(buscarDisponibilidadeF(request))
