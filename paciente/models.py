from django.db import models
from core.funcoes.enumerate import ESTADOS

class Paciente(models.Model):
    """
    *   Classe Paciente
    *   Base de uma paciente
    """
    ativo = models.BooleanField(verbose_name='Ativar Paciente ?', default=True, null=True)
    nomeCompleto = models.CharField(verbose_name='Nome Completo', max_length=120, null=True, blank=True)
    whatsapp = models.CharField(verbose_name='Whatsapp', max_length=120, null=True, blank=True)
    telefone = models.CharField(verbose_name='Telefone', max_length=120, null=True, blank=True)
    email = models.CharField(verbose_name='Email', max_length=120, null=True, blank=True, unique=True)
    cep = models.CharField(verbose_name='CEP', max_length=120, null=True, blank=True)
    cidade = models.CharField(verbose_name='Cidade', max_length=120, null=True, blank=True)
    estado = models.CharField(verbose_name='Estado', max_length=2, choices=ESTADOS, null=True, blank=True)
    redeSocial = models.CharField(verbose_name='Rede Social', max_length=120, null=True, blank=True)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return self.nomeCompleto
