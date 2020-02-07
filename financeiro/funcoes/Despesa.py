from django.db.models import Q
from ..models import Despesa as DespesaModel, Categoria
import logging

def criar(formulario):
    try:
        formulario['descricao'] = formulario['descricao'].upper()
        formulario['categoria'] = Categoria.objects.get(id=formulario['categoria'])
        formulario['data_vencimento'] = formulario['data_vencimento']
        formulario['valor'] = float(formulario['valor'])
        formulario['data_pagamento'] = formulario['data_pagamento']
        formulario['forma_pagamento'] = formulario['forma_pagamento']


        del formulario['id']

        DespesaModel.objects.create(**formulario)

        return {'status': True, 'msg': 'Feito lançamanto da Despesa com sucesso'}
    except ValueError as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Valor inválido']}
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Erro ao tentar lançar a Despesa']}


def editar(formulario):

    try:
        despesa = DespesaModel.objects.filter(id=formulario['id'])
        formulario['descricao'] = formulario['descricao'].upper()
        formulario['categoria'] = Categoria.objects.get(id=formulario['categoria'])
        formulario['data_vencimento'] = formulario['data_vencimento']
        formulario['valor'] = float(formulario['valor'])
        formulario['data_pagamento'] = formulario['data_pagamento']
        formulario['forma_pagamento'] = formulario['forma_pagamento']

        del formulario['id']

        despesa.update(**formulario)
        return {'status': True, 'msg': 'Despesa editado com sucesso'}
    except ValueError as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Valor inválido']}
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Erro ao tentar editar a despesa']}


def excluir(formulario):
    try:
        if formulario['id_excluir'] == formulario['id']:
            DespesaModel.objects.filter(pk=formulario['id']).delete()
            return {'status': True, 'msg': ['Despesa excluido com sucesso']}
        else:
            return {'status': False, 'msg': ['ID digitado nao confere com a Despesa selecionado']}
    except:
        return {'status': False, 'msg': ['Erro ao tentar excluir a Despesa']}


def criarEditarExcluirD(request):
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


def getDespesaString():
    """Monta as linhas da tabela em html e retorna em uma única string"""
    try:
        despesas = DespesaModel.objects.all().values('id', 'descricao', 'data_vencimento', 'valor')
        html = '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>'
        linhas = map(lambda p: html.format(p['id'], p['descricao'], p['data_vencimento'], p['valor']),
                     despesas)
        return "".join(list(linhas))
    except:
        print("Erro ao montar a lista de despesas")
        return ""


'''
    Métodos AJAX 
'''

def getDados(request):
    """Retorna uma receita buscando pelo ID"""
    try:
        id = request.GET.get("id")
        despesa = DespesaModel.objects.get(id=id)
        return {
            'status': True,
            'despesa': {
                'id_categoria': despesa.categoria.id,
                'descricao': despesa.descricao,
                'categoria': despesa.categoria.descricao,
                'data_vencimento': despesa.data_vencimento,
                'valor': despesa.valor,
                'data_pagamento': despesa.data_pagamento,
                'forma_pagamento': despesa.forma_pagamento,
            }
        }
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'despesa': {}, 'status': False, 'msg': ['Erro ao carregar a despesa']}

def getDespesas(request):
    """Retorna uma lista de despesa """
    q = request.GET.get('q', None)
    try:
        if q:
            return {'despesas': list(DespesaModel.objects.filter((Q(descricao__contains=q.upper()) | Q(categoria__contains=q.upper()) | Q(data_vencimento__contains=q) | Q(valor__contains=q) | Q(data_pagamento__contains=q)) & Q(forma_pagamento__contains=q))
                                     .values('id', 'descricao', 'categoria', 'data_vencimento', 'valor', 'data_pagamento', 'forma_pagamento'))
                    }
        else:
            return {
                'despesas': list(DespesaModel.objects.filter(ativo=True).values('id', 'descricao', 'categoria', 'data_vencimento', 'valor', 'data_pagamento', 'forma_pagamento'))
            }
    except:
        return {'despesas':[]}

def getCategorias(request):
    """Retorna uma lista de Categorias """
    q = request.GET.get('q', None)
    print(q)
    try:
        if q:
            return {'categorias': list(Categoria.objects.filter((Q(descricao__contains=q.upper())) & Q(ativo=True))
                                     .values('id', 'descricao'))
                    }
        else:
            return {
                'categorias': list(Categoria.objects.filter(ativo=True).values('id', 'descricao'))
            }
    except:
        return {'categorias':[]}
