from django.urls import path
from .views import *

urlpatterns = [
    path('cadastro/', Cadastro.pacienteView, name='cadastro_paciente'),
]