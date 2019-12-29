from django.urls import path
from .views import *

urlpatterns = [
    path('getProduto/', ProdutoAjax.getProduto, name='getProduto'),
    path('getProdutos/', ProdutoAjax.getProdutos, name='getProdutos'),
    path('', ProdutoView.produto, name='produto'),
]