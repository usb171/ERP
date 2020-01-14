from django.db import models
from core.funcoes.enumerate import FORMAS_PAGAMENTO


class Categoria(models.Model):
    """
    *   Classe Despesa
    """
    descricao = models.CharField(verbose_name='Descrição da categoria', max_length=120, default=True, null=True)
    observacao = models.CharField(verbose_name='Obsercao da categoria', max_length=120, default=True, null=True)

    def __str__(self):
        return self.descricao


class Despesa(models.Model):
    """
    *   Classe Despesa
    """
    descricao = models.CharField(verbose_name='Descrição da Despesa', max_length=120, default=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True)
    data_vencimento = models.CharField(verbose_name='Data do Vencimento', max_length=10, null=True, blank=False)
    valor = models.CharField(verbose_name='Valor da Despesa',  help_text='Valor da Despesa', max_length=8,
                               default='0', null=True)
    data_pagamento = models.CharField(verbose_name='Data de Pagamento', max_length=10, null=True, blank=False)
    forma_pagamento = models.CharField(verbose_name='Forma de Pagamento', help_text='Escolha a forma de pagamento', choices=FORMAS_PAGAMENTO,
                                       max_length=2, default='1')

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'

    def __str__(self):
        return self.descricao

