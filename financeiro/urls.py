from django.urls import path
from .views import *

urlpatterns = [
    path('getDados/', ReceitaAjax.getDados, name='getDados'),
    path('getReceitas/', ReceitaAjax.getReceitas, name='getReceitas'),
    path('', ReceitaView.receita, name='receita'),
]