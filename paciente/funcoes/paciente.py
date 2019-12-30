from ..models import Paciente as PacienteModel
from django.db.models import Q


def criar(formulario):
    try:
        formulario['cidade'] = formulario['cidade'].upper()
        formulario['nomeCompleto'] = formulario['nomeCompleto'].upper()
        del formulario['id']
        print(formulario)
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
        return ""


'''
    Métodos AJAX 
'''


def getPaciente(request):
    """Retorna um paciente buscando pelo ID"""
    try:
        id = request.GET.get("id")
        paciente = PacienteModel.objects.get(id=id)
        return {'paciente': {
            'nomeCompleto': paciente.nomeCompleto,
            'whatsapp': paciente.whatsapp,
            'telefone': paciente.telefone,
            'cidade': paciente.cidade,
            'endereco': paciente.endereco,
            'rg': paciente.rg,
            'instagram': paciente.instagram,
            'email': paciente.email,
        }
        }
    except:
        return {'paciente': {}}


def getPacientes(request):
    """Retorna uma lista de pacientes buscando por nome ou whatsapp ou email"""
    q = request.GET.get('q', None)
    try:
        if q:
            return {
                'pacientes': list(
                    PacienteModel.objects.filter((Q(nomeCompleto__contains=q.upper()) | Q(whatsapp__contains=q) |
                                                  Q(email__contains=q)) & Q(ativo=True))
                    .values('id', 'nomeCompleto', 'whatsapp', 'email'))
            }
        else:
            return {
                'pacientes': list(
                    PacienteModel.objects.filter(ativo=True).values('id', 'nomeCompleto', 'whatsapp', 'email'))
            }
    except:
        return {'pacientes': []}
