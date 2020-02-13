$("#id_nav_link_agenda").addClass("active");

// Mask ****************************************************************************************************************

$('[data-mask]').inputmask()

// Select2 *************************************************************************************************************

$("#paciente").select2({
    theme: 'bootstrap4',
    ajax: {
        url: "/paciente/getPacientes",
        dataType: 'json',
        delay: 100,
        data: function (params) {
                return {
                    q: params.term,
                };
        },
        processResults:function(data){
            return {
                results: $.map(data.pacientes, function (paciente) {
                            return {
                                id: paciente.id,
                                text: paciente.nomeCompleto,
                                email: paciente.email,
                                whatsapp: paciente.whatsapp
                            }
                         })
            };
        },
        cache: true
    },
    templateResult: formatPaciente,
    templateSelection: formatPacienteSelection
});

$('#paciente').on("change", function(e) {
    buscarDisponibilidade();
});

function formatPaciente (paciente) {
  if (paciente.loading) {
    return paciente.text;
  }

  var $container = $(
    "<div class='select2-result-repository clearfix'>" +
      "<div class='select2-result-repository__meta'>" +
        "<div class='select2-result-repository__title'></div>" +
        "<div class='select2-result-repository__statistics'>" +
          "<div class='select2-result-repository__email'><i class='fas fa-at'></i></div>" +
          "<div class='select2-result-repository__whatsapp'><i class='fab fa-whatsapp'></i> </div>" +
        "</div>" +
      "</div>" +
    "</div>"
  );

  $container.find(".select2-result-repository__title").text(paciente.text);
  $container.find(".select2-result-repository__email").append("     " +  paciente.email);
  $container.find(".select2-result-repository__whatsapp").append("      " + paciente.whatsapp);


  return $container;
}

function formatPacienteSelection (paciente) { return paciente.nomeCompleto || paciente.text; }


$("#procedimentos").select2({
    theme: 'bootstrap4',
    ajax: {
        url: "/servico/getServicos",
        dataType: 'json',
        delay: 100,
        data: function (params) {
                return {
                    q: params.term,
                };
        },
        processResults:function(data){
            return {
                results: $.map(data.servicos, function (servico) {
                            return {
                                id: servico.id,
                                text: servico.nome,
                                valor_total: servico.valor_total
                            }
                         })
            };
        },
        cache: true
    },
    templateResult: formatServico,
    templateSelection: formatServicoSelection
});

$('#procedimentos').on("change", function(e) {
    buscarDisponibilidade();
});

function formatServico (servico) {
  if (servico.loading) {
    return servico.text;
  }

  var $container = $(
    "<div class='select2-result-repository clearfix'>" +
      "<div class='select2-result-repository__meta'>" +
        "<div class='select2-result-repository__title'></div>" +
        "<div class='select2-result-repository__statistics'>" +
          "<div class='select2-result-repository__valor_total'>R$ </div>" +
        "</div>" +
      "</div>" +
    "</div>"
  );

  $container.find(".select2-result-repository__title").text(servico.text);
  $container.find(".select2-result-repository__valor_total").append("     " +  servico.valor_total);


  return $container;
}

function formatServicoSelection (servico) { return servico.nome || servico.text; }

$("#profissional").select2({
    theme: 'bootstrap4',
    ajax: {
        url: "/getContas/",
        dataType: 'json',
        delay: 100,
        data: function (params) {
                return {
                    q: params.term,
                };
        },
        processResults:function(data){
            return {
                results: $.map(data.contas, function (conta) {
                            return {
                                id: conta.id,
                                text: conta.nomeCompleto
                            }
                         })
            };
        },
        cache: true
    },
    templateResult: formatConta,
    templateSelection: formatContaSelection
});

function formatConta (conta) {
  if (conta.loading) {
    return conta.text;
  }

  var $container = $(
    "<div class='select2-result-repository clearfix'>" +
      "<div class='select2-result-repository__meta'>" +
        "<div class='select2-result-repository__title'></div>" +
      "</div>" +
    "</div>"
  );

  $container.find(".select2-result-repository__title").text(conta.text);


  return $container;
}

function formatContaSelection (conta) { return conta.username || conta.text; }

$('#profissional').on("change", function(e) {
    buscarDisponibilidade();
});

// Timepicker **********************************************************************************************************

$('#timepickerData').datetimepicker({
    format: 'DD/MM/YYYY',
    daysOfWeekDisabled: [0]
})

$('#timepickerData_editar').datetimepicker({
    format: 'DD/MM/YYYY',
    daysOfWeekDisabled: [0]
})

$("#timepickerData").on("change.datetimepicker", function (e) {
    buscarDisponibilidade();
});

$('#timepickerData_filtro').datetimepicker({
    format: 'DD/MM/YYYY',
    daysOfWeekDisabled: [0]
})

$("#timepickerData_filtro").on("change.datetimepicker", function (e) {
    carregarAgenda();
});

$("#agendamento_filtro").on("change.periodo", function (e) {
    carregarAgenda();
});

let initTimepickerHorario = (val) =>{
    $('#timepickerHorario').datetimepicker({
        format: 'HH:mm',
        stepping: val.stepping,
        enabledHours: val.enabledHours,
    });

    $('#timepickerHorario_editar').datetimepicker({
        format: 'HH:mm',
        stepping: val.stepping,
        enabledHours: val.enabledHours,
    });

    $("#timepickerHorario").on("change.datetimepicker", function (e) {
        let horario = $(this).data('date');
        buscarDisponibilidade();
        atualizarPeriodoPeloHorario(horario);
        posicionaRowScrollTabelaHorarios(horario);
    });

    $("#timepickerHorario").on("click", function (e) {
        let horario = $(this).data('date');
        buscarDisponibilidade();
        atualizarPeriodoPeloHorario(horario);
        posicionaRowScrollTabelaHorarios(horario);
    });
};


$("#periodo").on("change.periodo", function (e) {
    cod_periodo = $(this).val();
    buscarDisponibilidade();
    atualizarHorarioPeloPeriodo(cod_periodo)
});


let atualizarPeriodoPeloHorario = (horario) => {
    if (horario > '00:00' && horario < '12:00') $("#periodo").val('1');
    else if (horario >= '12:00' && horario < '19:00') $("#periodo").val('2');
    else if (horario >= '19:00') $("#periodo").val('3');
}

let atualizarHorarioPeloPeriodo = (cod_periodo) => {
    if (cod_periodo == 1) $('#timepickerHorario').datetimepicker("date", "07:00");
    else if (cod_periodo == 2) $('#timepickerHorario').datetimepicker("date", "12:00");
    else $('#timepickerHorario').datetimepicker("date", "19:00");
}

let posicionaRowScrollTabelaHorarios = (horario) => {
    $tableContainer = $('#tableContainer');
    $tableContainer.scrollTop(0)
    $tableContainer.scrollTop($(`td:contains('${horario}')`)[0].offsetTop - 50)
}

let carregarAgenda = (carregando=false) => {

    $data = $("#timepickerData_filtro");
    $agendamento = $("#agendamento_filtro");
    $financeiro = $("#financeiro_filtro");

    let formulario = {
        'data': $data.data('date'),
        'agendamento': $agendamento.val(),
        'financeiro': $data.data('$financeiro')
    }

    $.ajax({
        url: "/agenda/carregarAgenda",
        data: formulario,
        dataType: 'json',
        success: function (data) {
           $("#tabela_agendas tbody").html(data.agendas.linhas);
           if(carregando) EasyLoading.hide();
        }
    });
}

let buscarDisponibilidade = (carregando=false) =>{
    $periodo = $("#periodo");
    $paciente = $("#paciente");
    $data = $("#timepickerData");
    $profissional = $("#profissional");
    $horario = $("#timepickerHorario");
    $procedimentos = $("#procedimentos");

    let formulario = {
        'periodo': $periodo.val(),
        'paciente': $paciente.val(),
        'data': $data.data('date'),
        'profissional': $profissional.val(),
        'horario': $horario.data('date'),
        'procedimentos': $procedimentos.val(),
    }

    $.ajax({
        url: "/agenda/buscarDisponibilidade",
        data: formulario,
        dataType: 'json',
        success: function (data) {
           $("#tabela_horarios tbody").html(data.disponibilidade.linhas_horarios);
           if(carregando) EasyLoading.hide();
        }
    });
}

let agendar = (horario) => {

    EasyLoading.show({
        type: EasyLoading.TYPE["BALL_PULSE"],
        text: 'Agendando Paciente...',
        timeout: null,
    });

    $periodo = $("#periodo");
    $paciente = $("#paciente");
    $data = $("#timepickerData");
    $profissional = $("#profissional");
    $procedimentos = $("#procedimentos");
    $observacoes = $("#observacoes");

    let formulario = {
        'periodo': $periodo.val(),
        'paciente': $paciente.val(),
        'data': $data.data('date'),
        'profissional': $profissional.val(),
        'horario': horario,
        'procedimentos': $procedimentos.val(),
        'observacoes': $observacoes.val()
    }

    $.ajax({
        url: "/agenda/agendar",
        data: formulario,
        dataType: 'json',
        success: function (data) {
           $data.removeClass("is-invalid");
           $paciente.removeClass("is-invalid");
           $profissional.removeClass("is-invalid");
           $procedimentos.removeClass("is-invalid");
           if(data.flag){
                buscarDisponibilidade(carregando=true);
                carregarAgenda();
                $("#procedimentos").val(null).trigger("change");

           }else{
                if(data.erros.data){
                    $data.addClass("is-invalid")
                    toastr.error(data.erros.data)
                }else if(data.erros.paciente){
                    $paciente.addClass("is-invalid")
                    toastr.error(data.erros.paciente)
                }else if(data.erros.profissional){
                    $profissional.addClass("is-invalid")
                    toastr.error(data.erros.profissional)
                }else if(data.erros.procedimentos){
                    $procedimentos.addClass("is-invalid")
                    toastr.error(data.erros.procedimentos)
                }
                EasyLoading.hide();
           }
        }
    });


};
