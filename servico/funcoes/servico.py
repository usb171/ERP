from ..models import Servico as ServicoModel


def criar(formulario):
    try:
        formulario['nome'] = formulario['nome'].upper()
        formulario['tempo'] = formulario['tempo']
        formulario['valor_total'] = formulario['valor_total']
        formulario['valor_clinica'] = formulario['valor_clinica']
        formulario['valor_produtos'] = formulario['valor_produtos']
        formulario['produtos'] = formulario['produtos']
        del formulario['id']

        ServicoModel.objects.create(**formulario)
        return {'status': True, 'msg': 'Servico cadastrado com sucesso'}
    except:
        return {'status': False, 'msg': ['Erro ao tentar cadastrar o servico']}


def editar(formulario):
    try:
        servico = ServicoModel.objects.filter(id=formulario['id'])
        formulario['nome'] = formulario['nome'].upper()
        formulario['tempo'] = formulario['tempo']
        formulario['valor_total'] = formulario['valor_total']
        formulario['valor_clinica'] = formulario['valor_clinica']
        formulario['valor_produtos'] = formulario['valor_produtos']
        formulario['produtos'] = formulario['produtos']
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

    print(formulario)
    formulario = {k: str(v[0]) for k, v in dict(formulario).items() if isinstance(v, (list,))}
    print(formulario)

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


def getServico(request):
    """Retorna um serviço buscando pelo ID"""
    try:
        id = request.GET.get("id")
        paciente = ServicoModel.objects.get(id=id)
        return {'servico': {
            'nome': paciente.nome,
            'tempo': paciente.tempo,
            'valor_total': paciente.valor_total,
            'valor_clinica': paciente.valor_clinica,
            'valor_mao_obra': paciente.valor_mao_obra,
            'valor_produtos': paciente.valor_produtos,
            # 'produtos': paciente.produtos,
        }
        }
    except:
        return {'servico': {}}
