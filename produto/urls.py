from django.urls import path
from .views import *

urlpatterns = [
    path('getDados/', Produto_Ajax.getDados, name='getDados'),
    path('', ProdutoView.produto, name='produto'),
]