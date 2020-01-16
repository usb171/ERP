from django.contrib.auth.models import User, AbstractUser
from django.db.models import Q

from ..models import Conta
from .sessao import *


def alterarDados(formulario):
    try:
        conta = Conta.objects.filter(id=formulario['id'])
        formulario['nomeCompleto'] = formulario['nomeCompleto'].upper()
        del formulario['id']
        conta.update(**formulario)
        return {'status': True, 'msg': 'Conta editada com sucesso'}
    except Exception as e:
        return {'status': False, 'erros': ['Erro ao tentar editar conta']}


def criarEditarExcluirAlterarDadosAlterarSenha(request):
    formulario = request.POST.copy()
    comando = formulario['comando']
    del formulario['comando']
    del formulario['csrfmiddlewaretoken']

    formulario = {k: str(v[0]) for k, v in dict(formulario).items() if isinstance(v, (list,))}

    if comando == '#criar#':
        pass
    elif comando == '#editar#':
        pass
    elif comando == '#excluir#':
        pass
    elif comando == '#alterarDados#':
        return alterarDados(formulario)
    elif comando == '#alterarSenha#':
        return Sessao.alterar_senha(request)
    else:
        return {'status': False, 'msg': ['Não foi possível executar o comando: ' + str(comando)]}


def getContas(request):
    conta = request.GET.get('q', None)
    try:
        if conta:
            return {
                'contas': list(Conta.objects.filter(ativo=True, cargo='4', nomeCompleto__contains=conta.upper()).values('id', 'nomeCompleto'))
            }
        else:
            return {
                'contas': list(Conta.objects.filter(ativo=True, cargo='4').values('id', 'nomeCompleto'))
            }
    except Exception as e:
        print(e)
        return {'contas': []}

