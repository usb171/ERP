from ..models import Agenda as AgendaModel
from paciente.models import Paciente
from core.models import Conta
from servico.models import Servico
from django.db.models import Q
from datetime import datetime
from django.conf import settings
from core.funcoes.enumerate import PERIODO_AGENDA
import functools
import json


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
        acao = '<a href="#" id="agendar" onclick="{funcao}"> Agendar </a>'.format(
            funcao="agendar('{horario}');".format(horario=horario))
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


def agendar(request):
    try:
        lancar_erros = False
        erros = {'data': '', 'paciente': '', 'profissional': '', 'procedimentos': ''}
        data = request.GET.get("data")
        hora = request.GET.get("horario")
        periodo = request.GET.get("periodo")
        paciente = request.GET.get("paciente")
        profissional = request.GET.get("profissional")
        procedimentos = request.GET.get("procedimentos[]")

        if not data:
            erros['data'] = 'Data Inválida'
            lancar_erros = True
        elif not paciente:
            erros['paciente'] = 'Selecione o paciente'
            lancar_erros = True
        elif not profissional:
            erros['profissional'] = 'Selecione o profissional'
            lancar_erros = True
        elif not procedimentos:
            erros['procedimentos'] = 'Selecione pelo menos 1 procedimento'
            lancar_erros = True

        if lancar_erros: return {'flag': False, 'msg': 'Erro ao agendar paciente', 'erros': erros}

        formulario = {
            'status': '1',
            'hora': hora,
            'data': data,
            'periodo': periodo,
            'paciente': paciente,
            'profissional': profissional
        }

        formulario['paciente'] = Paciente.objects.get(id=formulario['paciente'])
        formulario['profissional'] = Conta.objects.get(id=formulario['profissional'])
        agendamento = AgendaModel.objects.create(**formulario)
        agendamento.procedimentos.set(Servico.objects.filter(id__in=dict(request.GET)['procedimentos[]']))
        return {'flag': True, 'msg': 'Paciente agendado com sucesso'}
    except Exception as e:
        return {'flag': False, 'msg': 'Erro ao agendar paciente {e}'.format(e=e)}


def buscarDisponibilidade(request):
    """Retorna um paciente buscando pelo ID"""
    try:
        periodo = request.GET.get("periodo")
        paciente = request.GET.get("paciente")
        data_form = request.GET.get("data")
        profissional = request.GET.get("profissional")
        hora_form = request.GET.get("horario")
        procedimentos = request.GET.get("procedimentos[]")
        agendas = AgendaModel.objects.filter(status='1', data=data_form, profissional=profissional)
        return {'disponibilidade': dict(linhas_horarios=get_linhas_tabela_horarios_html(agendas))}
    except Exception as e:
        print(e)
        return {'disponibilidade': dict()}
