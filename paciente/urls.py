from django.urls import path
from .views import *

urlpatterns = [
    path('lista/', Lista.listarPaciente, name='lista_paciente'),
    path('cadastro/', Cadastro.pacienteView, name='cadastro_paciente'),
    path('editar/', Cadastro.editarPaciente, name='editar_paciente'),

    path('getDados/', Paciente_Ajax.getDados, name='getDados'),
    path('', PacienteView.paciente, name='paciente'),
    path('buscarPacientes', PacienteView.buscarPacientes, name='buscarPacientes'),

]