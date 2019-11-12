from django.db import models
from django.contrib.auth.models import User

class Conta(models.Model):
    """
    *   Classe Conta
    *   Classe que extende a classe padrão `user` com objetivo de acrescentar mais atributos
    *   Atributos:
    *               ativo: Campo utilizado para ativar ou desativar uma conta
    """
    ativo = models.BooleanField(verbose_name='Ativar essa Conta ?', default=False, null=True)
    user = models.OneToOneField(User, verbose_name='Usuário de acesso', on_delete=models.SET_NULL, null=True)
    nomeCompleto = models.CharField('Nome Completo', max_length=120, null=True, blank=True)
    email = models.CharField('Email', max_length=120, null=True, blank=True, unique=True)
