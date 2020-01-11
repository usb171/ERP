from django.db import models
from paciente.models import Paciente
from core.models import Conta
from servico.models import Servico
from core.funcoes.enumerate import STATUS_AGENDA, PERIODO_AGENDA


class Agenda(models.Model):
    """
    *   Classe Agenda
    """
    status = models.CharField(verbose_name='Status', choices=STATUS_AGENDA, max_length=2, default='1')
    periodo = models.CharField(verbose_name='Período', choices=PERIODO_AGENDA, max_length=2, default='1')
    data = models.CharField(verbose_name='Data', max_length=10, null=True, blank=False)
    hora = models.CharField(verbose_name='Hora', max_length=5, null=True, blank=False)
    paciente = models.ForeignKey(Paciente, verbose_name='Paciente', on_delete=models.CASCADE)
    procedimentos = models.ManyToManyField(Servico, verbose_name='procedimentos')
    profissional = models.ForeignKey(Conta, verbose_name='Profissional', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Agenda'
        verbose_name_plural = 'Agendas'

    def __str__(self):
        return self.paciente.nomeCompleto
