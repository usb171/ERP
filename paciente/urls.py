from django.urls import path
from .views import Lista, Cadastro, Paciente_Ajax

urlpatterns = [
    path('lista/', Lista.listarPaciente, name='lista_paciente'),
    path('cadastro/', Cadastro.pacienteView, name='cadastro_paciente'),
    path('editar/', Cadastro.editarPaciente, name='editar_paciente'),
    path('paciente_retornar_dados/', Paciente_Ajax.retornarDados, name='retornar_dados'),
]