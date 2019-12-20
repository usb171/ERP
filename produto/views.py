from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from .forms import *
from .models import Produto as ProdutoModel, TIPO
from .funcoes.produto import getProdutoString


class Produto_Ajax():

    @login_required(login_url='login')
    def getDados(request):
        try:
            id = request.GET.get("id")
            produto = ProdutoModel.objects.get(id=id)
            contexto = {'nome_produto': produto.nome_produto,
                        'tipo_produto': produto.tipo_produto,
                        'quantidade_produto': produto.quantidade_produto,
                        'valor_produto': produto.valor_produto,
                        }
            return JsonResponse({'produto': contexto})
        except:
            return JsonResponse({'produto': 'Não foi possivel encontrar dados do produto de id' + id})

class ProdutoView():

    @login_required(login_url='login')
    def produto(request):
        template_name = "produto/produto.html"
        context = {'produtos': getProdutoString(), 'tipo_produto': list(map(lambda x: x[0], TIPO))}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return JsonResponse(ProdutoForm().criarEditarExcluir(request))
