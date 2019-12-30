from django.urls import path
from .views import *

urlpatterns = [
    path('getProduto/', ProdutoAjax.getProduto, name='getProduto'),
    path('getProdutos/', ProdutoAjax.getProdutos, name='getProdutos'),
    path('getValorTotal/', ProdutoAjax.getValorTotal, name='getValorTotal'),
    path('', ProdutoView.produto, name='produto'),
]