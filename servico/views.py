from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from servico.form import ServicoForm
from servico.funcoes.servico import getServicosString
from servico.models import Servico
from produto.models import Produto


class Servico_Ajax():
    @login_required(login_url='login')
    def getDados(request):
        try:
            id = request.GET.get("id")
            servico = Servico.objects.get(id=id)
            contexto = {'nome_servico': servico.nome_servico,
                        'valor_servico': servico.valor_servico,
                        'tempo_servico': servico.tempo_servico,
                        }

            return JsonResponse({'servico': contexto})
        except:
            return JsonResponse({'servico': 'Não foi possivel encontrar dados do serviço de id: ' + id})

class ServicoView():
    @login_required(login_url='login')
    def servico(request):
        template_name = "servico/servico.html"
        context = {'servicos': getServicosString(), 'produto_servico': Produto.objects.all()}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return JsonResponse(ServicoForm().criarEditarExcluir(request))
