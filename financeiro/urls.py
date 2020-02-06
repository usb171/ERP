from django.urls import path
from .views import *

urlpatterns = [
    path('getDados/', ReceitaAjax.getDados, name='getDados'),
    path('getReceitas/', ReceitaAjax.getReceitas, name='getReceitas'),
    path('receita/', ReceitaView.receita, name='receita'),
    path('getDadosDespesa/', DespesaAjax.getDados, name='getDadosDespesa'),
    path('getDespesas/', DespesaAjax.getDespesas, name='getDespesas'),
    path('despesa/', DespesasView.despesa, name='despesa'),
    path('getCategorias/', DespesaAjax.getCategorias, name='getCategorias'),
]
