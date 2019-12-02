from ..models import Paciente as PacienteModel
from django.core.paginator import Paginator
from django.db.models import Q
import operator
import functools

def criar(formulario):
    try:
        formulario['cidade'] = formulario['cidade'].upper()
        formulario['nomeCompleto'] = formulario['nomeCompleto'].upper()
        del formulario['id']
        PacienteModel.objects.create(**formulario)
        return {'status': True, 'msg': 'Paciente cadastrado com sucesso'}
    except Exception as e:
        return {'status': False, 'msg': ['Email já cadastrado']}


def editar(formulario):
    try:
        paciente = PacienteModel.objects.filter(id=formulario['id'])
        emailOriginal = paciente[0].email
        formulario['cidade'] = formulario['cidade'].upper()
        formulario['nomeCompleto'] = formulario['nomeCompleto'].upper()
        if emailOriginal != formulario["email"]:
            paciente.email = formulario["email"]
        del formulario['id']

        paciente.update(**formulario)
        return {'status': True, 'msg': 'Paciente editado com sucesso'}
    except Exception as e:
        return {'status': False, 'msg': ['Erro ao tentar editar paciente']}


def excluir(formulario):
    try:
        if formulario['id_excluir'] == formulario['id']:
            PacienteModel.objects.filter(pk=formulario['id']).delete()
            return {'status': True, 'msg': ['Paciente excluído com sucesso']}
        else:
            return {'status': False, 'msg': ['ID digitado não confere com o paciente selecionado']}
    except:
        return {'status': False, 'msg': ['Erro ao tentar excluir paciente']}


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
        return {'status': False, 'msg': ['Não foi possível executar o comando: ' + str(comando)]}


def getColunasTabela():
    colunas = [
                {'html': '<th style="width:5%">Cód.</th>', 'nomeVariavel': 'id'},
                {'html': '<th style="width:30%">Nome</th>', 'nomeVariavel': 'nomeCompleto'},
                {'html': '<th style="width:20%">Whatsapp</th>', 'nomeVariavel': 'whatsapp'},
                {'html': '<th style="width:20%">Telefône</th>', 'nomeVariavel': 'telefone'},
                {'html': '<th style="width:25%">E-mail</th>', 'nomeVariavel': 'email'}
              ]
    return colunas

def getColunasTabelaHtml():
    colunas = ''
    for coluna in list(map(operator.itemgetter('html'), getColunasTabela())):
        colunas = colunas + coluna
    return '<tr>{0}</tr>'.format(colunas)

def listarTabela(request):

    busca = request.GET.get('search[value]')
    start = request.GET.get('start')
    length = request.GET.get('length')

    pacientes_total = PacienteModel.objects.all()
    pacientes_filtro = pacientes_total.filter((Q(nomeCompleto__contains=busca.upper()) | Q(email__contains=busca)))

    '''Bloco da ordenação das colunas'''
    try:
        coluna = int(request.GET.get('order[0][column]'))
        tipo_ordem = request.GET.get('order[0][dir]')

        print(coluna)

        if tipo_ordem == 'desc':
            pacientes_filtro = pacientes_filtro.order_by(getColunasTabela()[coluna]['nomeVariavel'])
        elif tipo_ordem == 'asc':
            pacientes_filtro = pacientes_filtro.order_by('-' + getColunasTabela()[coluna]['nomeVariavel'])
    except:
        pacientes_filtro = pacientes_filtro.order_by('nomeCompleto')

    pacientes_filtro = pacientes_filtro.values('id', 'nomeCompleto', 'whatsapp', 'telefone', 'email')

    pagina = Paginator(pacientes_filtro, length)
    paginaAtual = int(start) / int(length) + 1
    pacientes_filtro = pagina.page(paginaAtual)
    pacientes_filtro = list(map(lambda paciente: list(paciente.values()), pacientes_filtro))
    total_pacientes = len(pacientes_total)
    return {"recordsTotal": total_pacientes, "recordsFiltered": total_pacientes, "data": pacientes_filtro}