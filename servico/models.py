from django.db import models
from produto.models import Produto


class Servico(models.Model):
    """
    *   Classe Servico
    *   Um serviço é composto de vários produtos de consumo
    *   O valor do serviço é composto do valor de quem realiza mais o valor do custo de todos os produtos
    """
    ativo = models.BooleanField(verbose_name='Ativar Servico ?', default=True, null=True)
    nome = models.CharField(verbose_name='Nome do serviço', max_length=120, default=True, null=True)
    tempo = models.CharField(verbose_name='Tempo de Serviço',
                             help_text='Tempo estimado em minutos para realizar o serviço', default='0', max_length=4,
                             null=True)

    valor_total = models.CharField(verbose_name='Valor total', help_text='Valor total do serviço', max_length=4,
                                   default='0', null=True)
    valor_clinica = models.CharField(verbose_name='Valor clínica', help_text='Valor de lucro da clínica', max_length=4,
                                     default='0', null=True)
    valor_mao_obra = models.CharField(verbose_name='Valor da mão de obra',
                                      help_text='Valor de custo do profissional para realizar o serviço', default='0',
                                      max_length=4, null=True)
    valor_produtos = models.CharField(verbose_name='Soma dos produtos', help_text='Soma de cada produto',
                                      max_length=4, default='0', null=True)

    produtos = models.ManyToManyField(Produto, help_text="Produtos selecionados para realizar o serviço", blank=True)

    class Meta:
        verbose_name = 'Servico'
        verbose_name_plural = 'Servicos'

    def __str__(self):
        return self.nome
