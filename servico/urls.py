from django.urls import path
from .views import *

urlpatterns = [
    path('getDados/', ServicoAjax.getDados, name='getDados'),
    path('getServicos/', ServicoAjax.getServicos, name='getServicos'),
    path('getValorTotal/', ServicoAjax.getValorTotal, name='getValorTotal'),
    path('', ServicoView.servico, name='servico'),
]
