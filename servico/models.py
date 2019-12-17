from django.db import models

class Servico(models.Model):
    """
            *   Classe Servico
            *   Base de uma serviço
            """
    ativo = models.BooleanField(verbose_name='Ativar Servico', default=True, null=True)
    nome_servico = models.CharField(verbose_name='Nome do serviço', max_length=120, default=True, null=True)
    valor_servico = models.DecimalField(verbose_name='Valor do serviço', max_digits=10, decimal_places=2, blank=True, null=True)
    tempo_servico = models.CharField(verbose_name='Tempo de Serviço', max_length=50, default=True)

    class Meta:
        verbose_name = 'Servico'
        verbose_name_plural = 'Servicos'

    def __str__(self):
        return self.nome_servico