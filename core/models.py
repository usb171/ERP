from django.db import models
from django.contrib.auth.models import User, Permission

CARGO = [
    ('1', 'GERENTE'),
    ('2', 'ADMINISTRADOR'),
    ('3', 'CAIXA'),
    ('4', 'DENTISTA'),
    ('5', 'ATENDENTE'),
    ('6', 'MANUTENÇÃO DO SISTEMA'),
]


class Conta(models.Model):
    """
    *   Classe Conta
    *   Classe que extende a classe padrão `user` com objetivo de acrescentar mais atributos
    *   Atributos:
    *               ativo: Campo utilizado para ativar ou desativar uma conta
    """
    ativo = models.BooleanField(verbose_name='Ativar essa Conta ?', default=False)
    user = models.OneToOneField(User, verbose_name='Usuário de acesso', on_delete=models.SET_NULL, null=True)
    nomeCompleto = models.CharField(verbose_name='Nome Completo', max_length=120, null=True, blank=True)
    cargo = models.CharField(verbose_name='Cargo', choices=CARGO, max_length=2, default='4', null=True)
    email = models.CharField(verbose_name='Email de acesso', help_text='E-mail tutilizado para acessar o sistema',
                             max_length=120, null=True, blank=True, unique=True)

    def __str__(self):
        return self.nomeCompleto
