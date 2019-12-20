from django.urls import path
from .views import *

urlpatterns = [
    path('getPaciente/', PacienteAjax.getPaciente, name='getPaciente'),
    path('getPacientes/', PacienteAjax.getPacientes, name='getPacientes'),
    path('', PacienteView.paciente, name='paciente'),
]