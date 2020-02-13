from django.urls import path
from .views import *

urlpatterns = [
    path('', AgendaView.agenda, name='agenda'),
    path('getDados/', AgendaAjax.getDados, name='getDados'),
    path('agendar', AgendaAjax.agendar, name='agendar'),
    path('carregarAgenda', AgendaAjax.carregarAgenda, name='carregarAgenda'),
    path('carregarAgenda', AgendaAjax.carregarAgenda, name='carregarAgenda'),
    path('buscarDisponibilidade', AgendaAjax.buscarDisponibilidade, name='buscarDisponibilidade'),
]