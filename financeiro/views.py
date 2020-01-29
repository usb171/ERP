from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from financeiro.form import ReceitaForm
from financeiro.funcoes.financeiro import getReceitasString, getDados as getDadosR, getReceitas as getReceitasR


class ReceitaAjax():
    @login_required(login_url='login')
    def getDados(request):
        try:
            return JsonResponse(getDadosR(request))
        except:
            return JsonResponse({'receita': 'Não foi possivel encontrar dados da receita de id: ' + id})

    @login_required(login_url='login')
    def getReceitas(request):
        return JsonResponse(getReceitasR(request))


class ReceitaView():
    @login_required(login_url='login')
    def receita(request):
        template_name = "financeiro/receita.html"
        context = {'receitas': getReceitasString()}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return JsonResponse(ReceitaForm().criarEditarExcluir(request))