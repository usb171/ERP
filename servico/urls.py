from django.urls import path
from .views import *

urlpatterns = [
    path('getDados/', Servico_Ajax.getDados, name='getDados'),
    path('', ServicoView.servico, name='servico'),
]