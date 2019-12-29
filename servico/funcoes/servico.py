from ..models import Servico as ServicoModel
import logging


def criar(formulario):
    try:
        formulario['nome'] = formulario['nome'].upper()
        formulario['valor_total'] = float(formulario['valor_total'])
        formulario['valor_clinica'] = float(formulario['valor_clinica'])
        formulario['valor_produtos'] = float(formulario['valor_produtos'])
        del formulario['id']
        del formulario['produtos']
        ServicoModel.objects.create(**formulario)
        return {'status': True, 'msg': 'Servico cadastrado com sucesso'}
    except ValueError as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Valor inválido']}
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Erro ao tentar cadastrar o servico']}


def editar(formulario):
    try:
        servico = ServicoModel.objects.filter(id=formulario['id'])
        formulario['nome'] = formulario['nome'].upper()
        formulario['valor_mao_obra'] = float(formulario['valor_mao_obra'])
        formulario['valor_clinica'] = float(formulario['valor_clinica'])
        formulario['valor_produtos'] = float(formulario['valor_produtos'])
        del formulario['id']
        # del formulario['produtos']
        servico.update(**formulario)
        return {'status': True, 'msg': 'Servico editado com sucesso'}
    except ValueError as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'status': False, 'msg': ['Valor inválido']}
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
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
        servicos = ServicoModel.objects.all().values('id', 'nome', 'valor_total', 'tempo')
        html = '<tr><td>{0}</td><td>{1}</td><td>R$ {2}</td><td>{3} Min</td>'
        linhas = map(lambda p: html.format(p['id'], p['nome'], p['valor_total'], p['tempo']),
                     servicos)
        return "".join(list(linhas))
    except:
        print("Erro ao montar a lista de servicos")
        return ""


'''
    Métodos AJAX 
'''


def getDados(request):
    """Retorna um serviço buscando pelo ID"""
    try:
        id = request.GET.get("id")
        paciente = ServicoModel.objects.get(id=id)
        return {
            'status': True,
            'servico': {
                'nome': paciente.nome,
                'tempo': paciente.tempo,
                'valor_total': paciente.valor_total,
                'valor_clinica': paciente.valor_clinica,
                'valor_mao_obra': paciente.valor_mao_obra,
                'valor_produtos': paciente.valor_produtos,
                # 'produtos': paciente.produtos,
            }
        }
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'servico': {}, 'status': False, 'msg': ['Erro ao carregar serviço']}
