from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from financeiro.form import ReceitaForm, DespesaForm
from financeiro.funcoes.financeiro import getReceitasString, getDados as getDadosR, getReceitas as getReceitasR
from financeiro.funcoes.Despesa import getDespesaString, getDados as getDadosD, getDespesas as getDespesasD, getCategorias as getCategoriasC


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
        context = {'receitas': getReceitasString(), 'options_forma_pagamento': '<option>DINHEIRO</option>,<option>DEBITO</option>,<option>CREDITO</option> '}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return JsonResponse(ReceitaForm().criarEditarExcluir(request))

class DespesaAjax():
    @login_required(login_url='login')
    def getDados(request):
        try:
            return JsonResponse(getDadosD(request))
        except:
            return JsonResponse({'despesa': 'Não foi possivel encontrar dados da despesa de id: ' + id})

    @login_required(login_url='login')
    def getDespesas(request):
        return JsonResponse(getDespesasD(request))

    @login_required(login_url='login')
    def getCategorias(request):
        return JsonResponse(getCategoriasC(request))


class DespesasView():
    @login_required(login_url='login')
    def despesa(request):
        template_name = "financeiro/despesa.html"
        context = {'despesas': getDespesaString(), 'options_forma_pagamento': '<option>DINHEIRO</option>,<option>DEBITO</option>,<option>CREDITO</option> '}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return JsonResponse(DespesaForm().criarEditarExcluir(request))

