from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from servico.form import ServicoForm
from servico.funcoes.servico import getServicosString, getDados as getDadosF


class ServicoAjax():
    @login_required(login_url='login')
    def getDados(request):
        try:
            return JsonResponse(getDadosF(request))
        except:
            return JsonResponse({'servico': 'Não foi possivel encontrar dados do serviço de id: ' + id})


class ServicoView():
    @login_required(login_url='login')
    def servico(request):
        template_name = "servico/servico.html"
        context = {'servicos': getServicosString()}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return JsonResponse(ServicoForm().criarEditarExcluir(request))
