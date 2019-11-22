from ..models import Produto as ProdutoModel

class Produto():
    """
        *  Método Produto
        *  Recebe o formulário da página do produto
        """
    def criarOuEditar(request):
        formulario = request.POST.copy()

        """ Caso seja um número, faça a edição do produto. Caso seja uma string vazia crie um produto"""
        if formulario['id'].isdigit():
            try:
                produto = ProdutoModel.objects.filter(id=formulario['id'])

                produto.update(
                    nome_produto=request.POST.get("nome_produto"),
                    valor_produto=request.POST.get("valor_produto")
                )
                return {'status': True, 'msg': 'Produto editado com sucesso'}
            except:
                return {'status': True, 'msg': 'Erro ao tentar editar paciente'}
        else:
            try:
                ProdutoModel.objects.create(
                    nome_produto=request.POST.get("nome_produto").upper(),
                    valor_produto=request.POST.get("valor_produto")
                )
                return {'status': True, 'msg': 'Produto cadastrado com sucesso'}
            except Exception as e:
                return {'status': False, 'mesg': ['Produto já cadastrado']}