from django.urls import path
from .views import *

urlpatterns = [
    path('lista/', PacienteList.as_view(), name='lista_paciente'),
    path('cadastro/', Cadastro.pacienteView, name='cadastro_paciente'),
    path('editar/', Cadastro.editarPaciente, name='editar_paciente'),
]