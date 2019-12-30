from django.db.models import Q
from ..models import Produto as ProdutoModel
import functools
import logging


def criar(formulario):
    try:
        formulario['nome'] = formulario['nome'].upper()
        formulario['tipo'] = formulario['tipo']
        formulario['quantidade'] = formulario['quantidade']
        formulario['valor'] = float(formulario['valor'])
        del formulario['id']
        ProdutoModel.objects.create(**formulario)
        return {'status': True, 'msg': 'Produto cadastrado com sucesso'}
    except ValueError as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'erros': {'valor': ['Valor inválido']}}
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Erro ao tentar cadastrar o produto']}


def editar(formulario):
    try:
        produto = ProdutoModel.objects.filter(id=formulario['id'])
        formulario['nome'] = formulario['nome'].upper()
        formulario['valor'] = float(formulario['valor'])
        del formulario['id']
        produto.update(**formulario)
        return {'status': True, 'msg': 'Produto editado com sucesso'}
    except ValueError as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'erros': {'valor': ['Valor inválido']}}
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Erro ao tentar editar produto']}


def excluir(formulario):
    try:
        if formulario['id_excluir'] == formulario['id']:
            ProdutoModel.objects.filter(pk=formulario['id']).delete()
            return {'status': True, 'msg': ['Produto excluido com sucesso']}
        else:
            return {'status': False, 'msg': ['ID digitado não confere com o produto selecionado']}
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Erro ao tentar excluir o produto']}


def criarEditarExcluir(request):
    formulario = request.POST.copy()
    comando = formulario['comando']
    del formulario['comando']
    del formulario['csrfmiddlewaretoken']

    formulario = {k: str(v[0]) for k, v in dict(formulario).items() if isinstance(v, (list,))}

    if comando == '#criar#':
        return criar(formulario)
    elif comando == '#editar#':
        return editar(formulario)
    elif comando == '#excluir#':
        return excluir(formulario)
    else:
        return {'status': False, 'msg': ['Não foi possivel executar o comando: ' + str(comando)]}


def getProdutoString():
    """Monta as linhas da tabela em html e retorna em uma única string"""
    try:
        produtos = ProdutoModel.objects.all().values('id', 'nome', 'tipo', 'quantidade', 'valor')
        html = '<tr><td>{0}</td><td>{1}</td><td>{3} {2}</td><td>R$ {4}</td>'
        linhas = map(lambda p: html.format(p['id'], p['nome'], p['tipo'], p['quantidade'], p['valor']), produtos)
        return "".join(list(linhas))
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return ""


def getProduto(request):
    """Retorna um produto pelo ID"""
    try:
        id = request.GET.get("id")
        produto = ProdutoModel.objects.get(id=id)
        return {
                'produto': dict(nome=produto.nome, tipo=produto.tipo, quantidade=produto.quantidade, valor=float(produto.valor)),
                'status': True
                }
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'produto': {}, 'status': False, 'msg': ['Erro ao carregar produto']}


def getValorTotal(request):
    """Retorna a soma total dos valores dos produtos selecionados pelo ID"""
    try:
        ids = request.GET.get("ids")
        soma = '0.00'
        if ids:
            produtos = ProdutoModel.objects.filter(id__in=ids.split(','))
            soma = sum(list(map(lambda p: float(p['valor']), produtos.values('valor'))))
        return {
                'valor': soma,
                'status': True
                }
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'produtos': {}, 'status': False, 'msg': ['Erro ao carregar produto']}


def getProdutos(request):
    """Retorna uma lista de produtos buscando por nome ou valor"""
    q = request.GET.get('q', None)
    try:
        if q:
            return {'produtos': list(
                ProdutoModel.objects.filter((Q(nome__contains=q.upper()) |
                                             Q(valor__contains=q)) & Q(ativo=True))
                    .values('id', 'nome', 'valor'))
            }
        else:
            return {
                'produtos': list(
                    ProdutoModel.objects.filter(ativo=True).values('id', 'nome', 'valor')
                )
            }
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'produtos': {}}
