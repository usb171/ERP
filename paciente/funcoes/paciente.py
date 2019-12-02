from ..models import Paciente as PacienteModel
import logging

logger = logging.getLogger(__name__)

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


def getPacientesString():
    """Monta as linhas da tabela em html e retorna em uma única string"""
    try:
        pacientes = PacienteModel.objects.all().values('id', 'nomeCompleto', 'whatsapp', 'telefone', 'email')
        html = '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>'
        linhas = map(lambda p: html.format(p['id'], p['nomeCompleto'], p['whatsapp'], p['telefone'], p['email']),
                     pacientes)
        return "".join(list(linhas))
    except:
        print("Erro ao montar lista de pacientes")
        logger.error('Erro ao montar lista de pacientes')
        return ""
