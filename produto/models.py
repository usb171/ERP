from django.db import models


class Produto(models.Model):
    """
        *   Classe Produto
        *   Base de uma produto ou serviço
        """
    ativo = models.BooleanField(verbose_name='Ativar Produto ?', default=True, null=True)
    nome_produto = models.CharField(verbose_name='Nome do produto', max_length=120, default=True, null=True)
    valor_produto = models.BooleanField(verbose_name='Valor do produto', default=True, null=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome_produto