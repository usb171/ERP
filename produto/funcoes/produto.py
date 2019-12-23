from django.db.models import Q

from ..models import Produto as ProdutoModel
import logging

logger = logging.getLogger(__name__)


def criar(formulario):
    try:
        formulario['nome_produto'] = formulario['nome_produto'].upper()
        formulario['tipo_produto'] = formulario['tipo_produto']
        formulario['quantidade_produto'] = formulario['quantidade_produto']
        formulario['valor_produto'] = formulario['valor_produto']
        del formulario['id']
        ProdutoModel.objects.create(**formulario)
        return {'status': True, 'msg': 'Produto cadastrado com sucesso'}
    except Exception as e:
        return {'status': False, 'msg': ['Erro ao tentar cadastrar o produto']}


def editar(formulario):
    try:
        produto = ProdutoModel.objects.filter(id=formulario['id'])
        formulario['nome_produto'] = formulario['nome_produto'].upper()
        formulario['tipo_produto'] = formulario['tipo_produto']
        formulario['quantidade_produto'] = formulario['quantidade_produto']
        formulario['valor_produto'] = formulario['valor_produto']
        del formulario['id']

        produto.update(**formulario)
        return {'status': True, 'msg': 'Produto editado com sucesso'}
    except:
        return {'status': False, 'msg': ['Erro ao tentar editar produto']}


def excluir(formulario):
    try:
        if formulario['id_excluir'] == formulario['id']:
            ProdutoModel.objects.filter(pk=formulario['id']).delete()
            return {'status': True, 'msg': ['Produto excluido com sucesso']}
        else:
            return {'status': False, 'msg': ['ID digitado não confere com o produto selecionado']}
    except:
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
        produtos = ProdutoModel.objects.all().values('id', 'nome_produto', 'tipo_produto', 'quantidade_produto', 'valor_produto')
        html = '<tr><td>{0}</td><td>{1}</td><td>{3} {2}</td><td>R$ {4}</td>'
        linhas = map(lambda p: html.format(p['id'], p['nome_produto'], p['tipo_produto'], p['quantidade_produto'],  p['valor_produto']), produtos)
        return "".join(list(linhas))
    except:
        print("Erro ao montar a lista de produtos")
        logger.error("Erro ao montar a lista de produtos")
        return ""

def getProduto(request):
    """Retorna um produto pelo ID"""
    try:
        id = request.GET.get("id")
        produto = ProdutoModel.objects.get(id=id)
        return {'produto':{
            'nome_produto': produto.nome_produto,
            'tipo_produto': produto.tipo_produto,
            'quantidade_produto': produto.quantidade_produto,
            'valor_produto': produto.valor_produto,
        }
        }
    except:
        return {'produto': {}}

def getProdutos(request):
    """Retorna uma lista de produtos buscando por nome ou valor"""
    q = request.GET.get('q', None)
    try:
        if q:
            return {'produtos': list(
                ProdutoModel.objects.filter((Q(nome_produto__contains=q.upper()) |
                                             Q(valor_produto__contains=q)) & Q(ativo=True))
                                            .values('id', 'nome_produto', 'valor_produto'))
            }
        else:
            return {
                'produtos': list(
                    ProdutoModel.objects.filter(ativo=True).values('id', 'nome_produto', 'valor_produto')
                )
            }
    except:
        return {'produtos': {}}