from ..models import Agenda as AgendaModel
from django.db.models import Q
from datetime import datetime
from django.conf import settings
from core.funcoes.enumerate import PERIODO_AGENDA
import functools
import json


#AGENDA='{ "INICIAL": 7, "FINAL": 19, "INTERVALO": 15, "PERIODOS": [1, 2] }'

def get_options_periodos():
    """Retorna os options conforme a configuração do arquivo de ambiente .env"""
    periodos = getattr(settings, 'AGENDA', '')['PERIODOS']
    periodos = list(map(lambda p: list(filter(lambda c: c[0] == str(p), PERIODO_AGENDA))[0], periodos))
    options = ''
    for p in periodos: options = options + '<option value="{value}">{text}</option>'.format(value=p[0], text=p[1])
    return options


def initTimepickerHorario():
    """Retorna as variáveis para iniciar o TimePickerHorario"""
    dict_agenda = getattr(settings, 'AGENDA', '')
    hora_inicial = dict_agenda['INICIAL']
    hora_final = dict_agenda['FINAL']
    intervalo = dict_agenda['INTERVALO']
    return json.dumps(dict(enabledHours=list(range(hora_inicial, hora_final + 1)), stepping=intervalo))


def get_lista_horarios():
    """Retorna uma lista com todos os horarios segundo o arquivo de ambiente .env"""
    try:
        dict_agenda = getattr(settings, 'AGENDA', '')
        horas = list(range(dict_agenda['INICIAL'], dict_agenda['FINAL'] + 1))
        intervalo = dict_agenda['INTERVALO']
        quant_intervalo = 60 / dict_agenda['INTERVALO']
        quant_intervalo = int(quant_intervalo) + 1 if quant_intervalo - int(quant_intervalo) > 0 else quant_intervalo

        lista_intervalos = []

        for h in horas:
            minutos = intervalo * -1
            for m in range(int(quant_intervalo)):
                minutos = int(minutos) + int(intervalo)
                minutos = '0' + str(minutos) if minutos < 10 else str(minutos)
                horas = '0' + str(h) if h < 10 else str(h)
                lista_intervalos.append(horas + ':' + minutos)

        return lista_intervalos
    except Exception as e:
        print(e)
        return []


def get_linhas_tabela_horarios_html(agendas):
    linhas = ''
    linha_html = '<tr {classe}>' \
                 '<td id={horario}>{horario}</td>' \
                 '<td>{profissional}</td>' \
                 '<td>{paciente}</td>' \
                 '<td>' \
                 '{acao}' \
                 '</td>' \
                 '</tr>'

    """Para cada horário possível da clínica"""
    for horario in get_lista_horarios():
        profissional = ''
        paciente = ''
        acao = '<a href="#"> Agendar </a>'
        classe = ''
        """Para cada agendamento encontrado para aquele dia verifique qual horário se encontra na lista de horários"""
        for agenda in agendas:
            if agenda.hora == horario:
                profissional = agenda.profissional.nomeCompleto
                paciente = agenda.paciente.nomeCompleto
                acao = '<a> Agendado </a>'
                classe = 'class="bg-info"'
                break
        linhas = linhas + linha_html.format(horario=horario, profissional=profissional, paciente=paciente,
                                            acao=acao, classe=classe)

    return linhas


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

        # agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S").split(' ')
        # data_agora = agora[0]
        # hora_agora = agora[1]

        # print(data_agora, hora_agora)
        # print(periodo, data_form, hora_form, paciente, profissional, procedimentos)

        agendas = AgendaModel.objects.filter(status='1', data=data_form)

        # print(list(map(lambda a: a.paciente, agendas)))

        return {'disponibilidade': dict(linhas_horarios=get_linhas_tabela_horarios_html(agendas))}
    except Exception as e:
        print(e)
        return {'disponibilidade': dict()}
