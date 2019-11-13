from ..models import Conta
from django.contrib.auth import authenticate, update_session_auth_hash, login as auth_login
from django.contrib.auth.forms import PasswordChangeForm

class Sessao():

    """
    *  Método Login
    *  Recebe email e senha, autentica e loga o usuário a uma nova sessão
    """
    def login(email, senha, request):
        context = {
            'logado': True,
            'msg': '',
            'email': email,
            'senha': senha
        }

        '''Busque a conta que contenha o email em questão'''
        try:
            conta = Conta.objects.get(email=email)
            ativo = conta.ativo

            if ativo:
                user = conta.user
                '''Faça a autenticação do usuário'''
                user = authenticate(request, username=user.username, password=senha)  # Faz a autenticação do usuário
                '''Se o usuário existir e for autenticado'''
                if user is not None:
                    auth_login(request, user)
                else:
                    context['msg'] = 'Não foi possível autenticar o usuário'
                    context['logado'] = False
            else:
                context['msg'] = 'Conta desativada'
                context['logado'] = False
        except:
            context['msg'] = 'E-mail não encontrado'
            context['logado'] = False

        return context

    def alterar_senha(request):
        context = {
            'alterado': True,
            'msg': '',
            'erros': None,
        }

        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            context['msg'] = "Atualizado com sucesso"
            return context
        else:
            context['alterado'] = False
            context['erros'] = form.errors
            context['msg'] = "Erro nos seguintes campos"
            return context
