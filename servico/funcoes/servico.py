from ..models import Servico as ServicoModel
import logging

logger = logging.getLogger(__name__)


def criar(formulario):
    try:
        formulario['nome_servico'] = formulario['nome_servico'].upper()
        formulario['valor_servico'] = formulario['valor_servico']
        formulario['tempo_servico'] = formulario['tempo_servico']
        del formulario['id']
        ServicoModel.objects.create(**formulario)
        return {'status': True, 'msg': 'Servico cadastrado com sucesso'}
    except Exception as e:
        return {'status': False, 'msg': ['Erro ao tentar cadastrar o servico']}


def editar(formulario):
    try:
        servico = ServicoModel.objects.filter(id=formulario['id'])
        formulario['nome_servico'] = formulario['nome_servico'].upper()
        formulario['valor_servico'] = formulario['valor_servico']
        formulario['tempo_servico'] = formulario['tempo_servico']
        del formulario['id']

        servico.update(**formulario)
        return {'status': True, 'msg': 'Servico editado com sucesso'}
    except:
        return {'status': False, 'msg': ['Erro ao tentar editar servico']}


def excluir(formulario):
    try:
        if formulario['id_excluir'] == formulario['id']:
            ServicoModel.objects.filter(pk=formulario['id']).delete()
            return {'status': True, 'msg': ['Servico excluido com sucesso']}
        else:
            return {'status': False, 'msg': ['ID digitado não confere com o servico selecionado']}
    except:
        return {'status': False, 'msg': ['Erro ao tentar excluir o servico']}


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

def getServicosString():
    """Monta as linhas da tabela em html e retorna em uma única string"""
    try:
        servicos = ServicoModel.objects.all().values('id', 'nome_servico', 'valor_servico', 'tempo_servico')
        html = '<tr><td>{0}</td><td>{1}</td><td>R$ {2}</td><td>{3}</td>'
        linhas = map(lambda p: html.format(p['id'], p['nome_servico'], p['valor_servico'], p['tempo_servico']), servicos)
        return "".join(list(linhas))
    except:
        print("Erro ao montar a lista de servicos")
        logger.error("Erro ao montar a lista de servicos")
        return ""