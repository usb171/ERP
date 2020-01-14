from django.urls import path
from .views import *

urlpatterns = [
    path('', AgendaView.agenda, name='agenda'),
    path('agendar', AgendaAjax.agendar, name='agendar'),
    path('buscarDisponibilidade', AgendaAjax.buscarDisponibilidade, name='buscarDisponibilidade'),
]