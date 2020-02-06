from django.db.models import Q
from ..models import Receita as ReceitaModel
from paciente.models import Paciente
from servico.models import Servico
import functools
import logging

def criar(formulario):
    try:
        formulario['paciente'] = Paciente.objects.get(id=formulario['paciente'])
        formulario['valor_apagar'] = float(formulario['valor_apagar'])
        formulario['forma_pagamento'] = formulario['forma_pagamento'].upper()
        procedimentos = Servico.objects.filter(id__in=formulario['procedimentos'].split(','))
        del formulario['id']
        del formulario['procedimentos']
        receita = ReceitaModel.objects.create(**formulario)
        receita.procedimentos.add(*procedimentos)
        receita.save()

        return {'status': True, 'msg': 'Feito lançamanto com sucesso'}
    except ValueError as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Valor inválido']}
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Erro ao tentar lançar o pagamento']}


def editar(formulario):

    try:
        receita = ReceitaModel.objects.filter(id=formulario['id'])
        formulario['paciente'] = Paciente.objects.get(id=formulario['paciente'])
        formulario['valor_apagar'] = float(formulario['valor_apagar'])
        formulario['forma_pagamento'] = formulario['forma_pagamento'].upper()

        if formulario['procedimentos']:
            procedimentos = Servico.objects.filter(id__in=formulario['procedimentos'].split(','))
            receita[0].procedimentos.clear()
            receita[0].procedimentos.add(*procedimentos)
        else:
            receita[0].procedimentos.clear()

        del formulario['id']
        del formulario['procedimentos']

        receita.update(**formulario)
        return {'status': True, 'msg': 'Receita editado com sucesso'}
    except ValueError as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Valor inválido']}
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Erro ao tentar editar a receita']}


def excluir(formulario):
    try:
        if formulario['id_excluir'] == formulario['id']:
            ReceitaModel.objects.filter(pk=formulario['id']).delete()
            return {'status': True, 'msg': ['Receita excluido com sucesso']}
        else:
            return {'status': False, 'msg': ['ID digitado nao confere com o lancamento selecionado']}
    except:
        return {'status': False, 'msg': ['Erro ao tentar excluir o lançamento']}


def criarEditarExcluir(request):
    formulario = request.POST.copy()
    comando = formulario['comando']
    del formulario['comando']
    del formulario['csrfmiddlewaretoken']

    formulario = {k: v[0] for k, v in dict(formulario).items() if isinstance(v, (list,))}

    if comando == '#criar#':
        return criar(formulario)
    elif comando == '#editar#':
        return editar(formulario)
    elif comando == '#excluir#':
        return excluir(formulario)
    else:
        return {'status': False, 'msg': ['Não foi possivel executar o comando: ' + str(comando)]}


def getReceitasString():
    """Monta as linhas da tabela em html e retorna em uma única string"""
    try:
        receitas = ReceitaModel.objects.all().values('id', 'paciente', 'valor_apagar', 'forma_pagamento')
        html = '<tr><td>{0}</td><td>{1}</td><td>R$ {2}</td><td>{3}</td>'
        linhas = map(lambda p: html.format(p['id'], Paciente.objects.get(id=p['paciente']).nomeCompleto, p['valor_apagar'], p['forma_pagamento']),
                     receitas)
        return "".join(list(linhas))
    except:
        print("Erro ao montar a lista de receitas")
        return ""


'''
    Métodos AJAX 
'''

def getDados(request):
    """Retorna uma receita buscando pelo ID"""
    try:
        id = request.GET.get("id")
        receita = ReceitaModel.objects.get(id=id)
        return {
            'status': True,
            'receita': {
                'id_paciente': receita.paciente.id,
                'paciente': receita.paciente.nomeCompleto,
                'procedimentos': list(receita.procedimentos.all().values('id', 'nome', 'valor_total')),
                'valor_apagar': receita.valor_apagar,
                'forma_pagamento': receita.forma_pagamento,
            }
        }
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'receita': {}, 'status': False, 'msg': ['Erro ao carregar a receita']}

def getReceitas(request):
    """Retorna uma lista de receita """
    q = request.GET.get('q', None)
    try:
        if q:
            return {'receitas': list(ReceitaModel.objects.filter((Q(paciente__contains=q.upper()) | Q(procedimentos__contains=q.upper()) | Q(valor_apagar__contains=q)) & Q(forma_pagamento__contains=q))
                                     .values('id', 'paciente', 'procedimentos', 'valor_apagar', 'forma_pagamento'))
                    }
    except:
        return {'receitas':[]}
