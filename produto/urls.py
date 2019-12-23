from django.urls import path
from .views import *

urlpatterns = [
    path('getProduto/', Produto_Ajax.getProduto, name='getProduto'),
    path('getProdutos/', Produto_Ajax.getProdutos, name='getProdutos'),
    path('', ProdutoView.produto, name='produto'),
]