from django.shortcuts import render

from produto.models import Produto


class Cadastro():

    def produtoView(request):
        template_name = 'produto/cadastro_produto.html'
        produtos = Produto.objects.all()
        contexto = {'produtos': []}

        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=contexto )
        elif request.method == 'POST':
            return render(request=request, template_name=template_name, context=contexto)
