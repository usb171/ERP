from django.urls import path
from .views import *

urlpatterns = [
    path('getDados/', Paciente_Ajax.getDados, name='getDados'),
    path('', PacienteView.paciente, name='paciente'),
    path('buscarPacientes', PacienteView.buscarPacientes, name='buscarPacientes'),
]