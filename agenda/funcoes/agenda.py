from ..models import Agenda as AgendaModel
from django.db.models import Q
from datetime import datetime

'''
    Métodos AJAX 
'''


def buscarDisponibilidade(request):
    """Retorna um paciente buscando pelo ID"""
    try:
        periodo = request.GET.get("periodo")
        paciente = request.GET.get("paciente")
        data_form = request.GET.get("data")
        profissional = request.GET.get("profissional")
        hora_form = request.GET.get("horario")
        procedimentos = request.GET.get("procedimentos")

        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S").split(' ')
        data_agora = agora[0]
        hora_agora = agora[1]

        print(data_agora, hora_agora)
        print(periodo, data_form, hora_form, paciente, profissional, procedimentos)

        return {'disponibilidade': dict()}
    except Exception as e:
        print(e)
        return {'disponibilidade': dict()}