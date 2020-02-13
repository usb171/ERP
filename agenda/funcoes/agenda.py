from ..models import Agenda as AgendaModel
from paciente.models import Paciente
from core.models import Conta
from servico.models import Servico
from django.db.models import Q
from datetime import datetime
from django.conf import settings
from core.funcoes.enumerate import PERIODO_AGENDA, STATUS_AGENDA, CORES_AGENDA
import functools
import json
import logging


def get_options_periodos():
    """Retorna os options conforme a configuração do arquivo de ambiente .env"""
    periodos = getattr(settings, 'AGENDA', '')['PERIODOS']
    periodos = list(map(lambda p: list(filter(lambda c: c[0] == str(p), PERIODO_AGENDA))[0], periodos))
    options = ''
    for p in periodos: options = options + '<option value="{value}">{text}</option>'.format(value=p[0], text=p[1])
    return options


def get_options_status():
    """Retorna os status em options possíveis para um agendamento"""
    options = ''
    for p in STATUS_AGENDA:
        options = options + '<option value="{value}">{text}</option>'.format(value=p[0], text=p[1])
    return options


def get_status(id):
    return list(filter(lambda s: s[0] == str(id), STATUS_AGENDA))[0][1]

def get_cor(id):
    return list(filter(lambda s: s[0] == str(id), CORES_AGENDA))[0][1]


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


def get_linhas_tabela_agenda_html(agendas):

    try:
        agendas = agendas.values('id', 'hora', 'paciente__nomeCompleto', 'profissional__nomeCompleto', 'status')
        html = '<tr onclick="carregarAgendamento({id})" style="cursor:pointer; background-color:{cor};" ><td>{hora}</td><td>{paciente}</td><td>{profissional}</td><td>{status}</td></tr>'

        return "".join(list(map(lambda a: html.format(id=a['id'],
                                                      hora=a['hora'],
                                                      paciente=a['paciente__nomeCompleto'],
                                                      profissional=a['profissional__nomeCompleto'],
                                                      status=get_status(a['status']),
                                                      cor=get_cor(a['status'])), agendas)))
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        print("Erro ao montar lista de linhas", e)
        return ""


def editarAgendamento(request):
    """ Edita um agendamento pelo ID
        Status: AGENDADO = 1, FINALIZADO = 2, EM ESPERA = 3, CANCELADO = 4, EM ATENDIMENTO = 5, REAGENDADADO = 6
    """
    try:
        post_dict = dict(request.POST)
        id = request.POST.get('id_editar_agendamento')
        status = request.POST.get("status_editar")
        hora = request.POST.get("hora_editar")
        data = request.POST.get("data_editar")
        profissional = request.POST.get("profissional_editar")
        id_profissional = request.POST.get("id_profissional_agendamento")
        procedimentos = post_dict.get("procedimentos_editar")
        observacoes = request.POST.get("observacoes_editar")

        formulario = {'status': status, 'hora': hora, 'data': data, 'observacoes': observacoes}
        agendamento = AgendaModel.objects.filter(id=id)

        """ Se o agendamento não for finalizado ou cancelado """
        if status not in ['2', '4']:
            if procedimentos:
                procedimentos = Servico.objects.filter(id__in=procedimentos)
                agendamento[0].procedimentos.clear()
                agendamento[0].procedimentos.add(*procedimentos)
            else:
                agendamento[0].procedimentos.clear()
        if status == '6':
           formulario['status'] = '1'


        """ Se o agendamento for finalizado ou cancelado
            Teste se é possível mudar o status do agendamento
        """
        if status not in ['2', '4']:
            """ Existe algum agendamento na mesma hora, data, profissional e status diferente de finalizado ou cancelado ? """
            agendamento_marcado = AgendaModel.objects.filter(Q(hora=hora, data=data, profissional=id_profissional)).exclude(id=id).exclude(status__in=['2', '4'])

            # print(id, hora, data, status, agendamento, agendamento_marcado)
            if agendamento_marcado:
                return {'status': False, 'msg': ["Encontramos um agendamento em {data} às {hora}".format(data=data, hora=hora)]}

        agendamento.update(**formulario)

        return {'status': True, 'msg': ['Agendamento alterado com sucesso']}
    except Exception as e:
        return {'status': False, 'msg': [str(e)]}

'''
    Métodos AJAX 
'''

def getDados(request):
    """Retorna um agendamento buscando pelo ID"""
    try:
        id = request.GET.get("id")
        agenda = AgendaModel.objects.get(id=id)
        return {
            'status': True,
            'agendamento': {
                'status': agenda.status,
                'data': agenda.data,
                'hora': agenda.hora,
                'paciente': agenda.paciente.nomeCompleto,
                'profissional': {'id': agenda.profissional.id, 'nomeCompleto': agenda.profissional.nomeCompleto},
                'procedimentos': list(agenda.procedimentos.all().values('id', 'nome')),
                'observacoes': agenda.observacoes
            }
        }
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return {'servico': {}, 'status': False, 'msg': ['Erro ao carregar serviço']}


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
        observacoes = request.GET.get("observacoes")

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
            'profissional': profissional,
            'observacoes': observacoes
        }

        formulario['paciente'] = Paciente.objects.get(id=formulario['paciente'])
        formulario['profissional'] = Conta.objects.get(id=formulario['profissional'])
        agendamento = AgendaModel.objects.create(**formulario)
        agendamento.procedimentos.set(Servico.objects.filter(id__in=dict(request.GET)['procedimentos[]']))
        return {'flag': True, 'msg': 'Paciente agendado com sucesso'}
    except Exception as e:
        return {'flag': False, 'msg': 'Erro ao agendar paciente {e}'.format(e=e)}


def carregarAgenda(request):
    """Carrega todos os agendamentos segundo os filtros"""
    try:
        data = request.GET.get("data")
        agendamento = request.GET.get("agendamento")
        financeiro = request.GET.get("financeiro")

        if agendamento == '0':
            agendas = AgendaModel.objects.order_by("hora").filter(data=data)
        else:
            agendas = AgendaModel.objects.order_by("hora").filter(status__contains=agendamento, data=data)
        return {'agendas': dict(linhas=get_linhas_tabela_agenda_html(agendas))}
    except Exception as e:
        return {'agendas': dict()}


def buscarDisponibilidade(request):
    """Retorna as linhas em html da tabela de disponibilidade daquele profissional"""
    try:
        data_form = request.GET.get("data")
        profissional = request.GET.get("profissional")
        agendas = AgendaModel.objects.filter(status__in=['1', '3', '5'], data=data_form, profissional=profissional)
        return {'disponibilidade': dict(linhas_horarios=get_linhas_tabela_horarios_html(agendas))}
    except Exception as e:
        return {'disponibilidade': dict()}
