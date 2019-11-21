from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from .forms import *

from produto.models import Produto


class ProdutoView():

    @login_required(login_url='login')
    def produto(request):
        template_name = "produto/produto.html"
        context = {'produto': []}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return JsonResponse(ProdutoForm().criarOuEditar(request))

    @login_required(login_url='login')
    def buscarProdutos(request):

        busca = request.GET.get('search[value]')
        produtos_total = Produto.objects.all()
        produtos_filtro = Produto.objects.filter(
            (Q(nome_produto__contains=busca) | Q(valor_produto__contains=busca))).order_by('nome_produto')\
            .values('id', 'nome_produto', 'valor_produto')

        produtos_filtro = list(map(lambda produto: list(produto.values()), produtos_filtro))

        context = {"recordsTotal": len(produtos_total),
                   "recordsFiltered": len(produtos_filtro),
                   "data": produtos_filtro}

        return JsonResponse(context)