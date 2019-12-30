from django.db import models

TIPO = [
    ('UN', 'Unidade'),
    ('LT', 'litro'),
    ('CX', 'Caixa'),
    ('M', 'Metro'),
]

class Produto(models.Model):
    """
    *   Classe Produto
    *   Base de uma produto
    """
    ativo = models.BooleanField(verbose_name='Ativar Produto ?', default=True, null=True)
    nome = models.CharField(verbose_name='Nome do produto', max_length=120, null=True)
    tipo = models.CharField(verbose_name='Unidade da Medida', choices=TIPO, max_length=3, default='UN', null=True)
    valor = models.CharField(verbose_name='Valor do produto', max_length=8, default='0', null=True)
    quantidade = models.CharField(verbose_name='Quantidade', max_length=4, default='1', null=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome