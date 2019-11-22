from ..models import Produto as ProdutoModel


def criar(formulario):
    try:
        formulario['nome_produto'] = formulario['nome_produto'].upper
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
