from django.db import models
TIPO = [
    ('UN', 'UN'),
    ('LT', 'LT'),
    ('CX', 'CX'),
    ('M', 'M'),
]

class Produto(models.Model):
    """
        *   Classe Produto
        *   Base de uma produto
        """
    ativo = models.BooleanField(verbose_name='Ativar Produto ?', default=True, null=True)
    nome_produto = models.CharField(verbose_name='Nome do produto', max_length=120, default=True, null=True)
    tipo_produto = models.CharField(verbose_name='Unidade de Medida', choices=TIPO, max_length=20, default='UN', null=True)
    valor_produto = models.DecimalField(verbose_name='Valor do produto', max_digits=10, decimal_places=2, blank=True, null=True)
    quantidade_produto = models.DecimalField(verbose_name='Quantidade', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome_produto