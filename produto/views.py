from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from .forms import *
from .models import TIPO
from .funcoes.produto import getProdutoString, getProduto as getProdutoF, getProdutos as getProdutosF


class ProdutoAjax():

    @login_required(login_url='login')
    def getProduto(request):
        return JsonResponse(getProdutoF(request))

    @login_required(login_url='login')
    def getProdutos(request):
        return JsonResponse(getProdutosF(request))


class ProdutoView():

    @login_required(login_url='login')
    def produto(request):
        template_name = "produto/produto.html"
        context = {'produtos': getProdutoString(), 'tipo_produto': list(map(lambda x: x[0], TIPO))}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return JsonResponse(ProdutoForm().criarEditarExcluir(request))
