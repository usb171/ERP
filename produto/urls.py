from django.urls import path
from .views import *

urlpatterns = [
    path('', ProdutoView.produto, name='produto'),
    path('buscarProdutos', ProdutoView.buscarProdutos, name='buscarProdutos'),
    path('getDados/', Produto_Ajax.getDados, name='getDados'),
]