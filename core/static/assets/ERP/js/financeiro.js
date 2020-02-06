$('[data-mask]').inputmask();

$('#valor_servicos').inputmask('decimal', {
                'integerDigits': 5,
                'alias': 'numeric',
                'autoGroup': true,
                'digits': 2,
                'digitsOptional': false,
                'allowMinus': false,
                'placeholder': ''
});

$('#valor_total').inputmask('decimal', {
                'integerDigits': 5,
                'alias': 'numeric',
                'autoGroup': true,
                'digits': 2,
                'digitsOptional': false,
                'allowMinus': false,
                'placeholder': ''
});


$("#id_nav_treeview_configuracoes_receita").addClass("menu-open");
$("#id_nav_link_receita").addClass("active");

/****************************************************** Tabela ********************************************************/
let table = $("#id_table_financeiro").DataTable({

    dom:"<'row be-datatable-header'<'col-sm-6'B><'col-sm-6'f>>" +
        "<'row be-datatable-body'<'col-sm-12'tr>>" +
        "<'row be-datatable-footer'<'col-sm-5'i><'col-sm-7'p>>",

    buttons: [
        {
            text: 'Novo',
            action: function ( e, dt, node, config ) {
                limparform();
                let comando = '#criar#'
                $('#id_modal_financeiro_novo_editar').modal('show');
                $("#comando_novo_editar").val(comando);
            },
            className: 'btn btn-success'
        },
        {
            text: 'Editar',
            action: function ( e, dt, node, config ) {
                EasyLoading.show({type: EasyLoading.TYPE["BALL_PULSE"], text: 'Carregando dados...', timeout: null,});
                let id = table.rows({selected:true}).data()[0][0]
                carregarDadosLinhaSelecionada(id);
                limparform();
                let comando = '#editar#'
                $('#id_modal_financeiro_novo_editar').modal('show');
                $("#comando_novo_editar").val(comando);
                EasyLoading.hide();
            },
            className: 'btn btn-warning',
            enabled: false
        },
        {
            text: 'Excluir',
            action: function ( e, dt, node, config ) {
                let linha = table.rows({selected:true}).data()[0];
                let id = linha[0];
                let nome = linha[1];
                $('#id_modal_financeiro_excluir').modal('show');
                $("#id_excluir").val('');
                $("#codigo_excluir_financeiro").text(id);
                $("#id_financeiro_selecionado").val(id);
                $("#nome_excluir_receita").text(nome);
            },
            className: 'btn btn-danger',
            enabled: false
        },
        {
            text: 'Exportar PDF',
            className: 'btn btn-primary',
            extend: 'pdfHtml5',
            messageTop: 'Nilton Nonato Garcia Júnior',
            download: 'open',
        }
    ],

    select: 'single',
    "processing": true,
    "serverSide": false,
    "bLengthChange": false,
    "pageLength": 10,
    "ordering": true,
    "info":     true,

    "language": {
        "sEmptyTable": "Nenhum registro encontrado",
        "sInfo": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
        "sInfoEmpty": "Mostrando 0 até 0 de 0 registros",
        "sInfoFiltered": "(Filtrados de _MAX_ registros)",
        "sInfoPostFix": "",
        "sInfoThousands": ".",
        "sLengthMenu": "_MENU_ resultados por página",
        "sLoadingRecords": "Carregando...",
        "sProcessing": "Buscando Pacientes ...",
        "sZeroRecords": "Nenhum paciente encontrado",
        "sSearch": "Pesquisar",
        "oPaginate": {
        "sNext": "Próximo",
        "sPrevious": "Anterior",
        "sFirst": "Primeiro",
        "sLast": "Último"
    },
    "oAria": {
        "sSortAscending": ": Ordenar colunas de forma ascendente",
        "sSortDescending": ": Ordenar colunas de forma descendente"
        }
    },
});

table.on( 'select deselect', function () {
    let selectedRows = table.rows( { selected: true } ).count();
    linha = table.rows({selected:true}).data()[0];
    table.button(1).enable( selectedRows > 0 );
    table.button(2).enable( selectedRows > 0 );
});
/****************************************************** Tabela ********************************************************/


/*************************************************** Formulários ******************************************************/


let carregarDadosLinhaSelecionada = (id) => {
    $.ajax({
        url: "/financeiro/getDados/",
        data: {'id': id},
        dataType: 'json',
        success: function (data) {
            receita = data.receita;
            status = data.status;
            if(data.status){
                $('#id').val(id);
                var newOption = new Option(receita.paciente, receita.id_paciente, false, false);
                $('#paciente').append(newOption).trigger('change');
                $('#paciente').val(receita.id_paciente).trigger('change');
                $('#valor_servicos').val(receita.valor_apagar);
                $('#forma_pagamento').val(receita.forma_pagamento);
                $("#id_criar_editar").val(id);
                $procedimentos = $('#procedimentos');
                $.each(receita.procedimentos, (index, servico) => {
                    $procedimentos.append(new Option(servico.nome, servico.id, true, true)).trigger('change');
                })
            }else{
                $.each(data.msg, (index, erro) => {
                    toastr.error(erro)
                })
            }
        }
    });
}
let limparform = () => {
    $('#paciente').val(null).trigger('change');
    $('#procedimentos').empty();
    $('#valor_apagar').val('');
    $('#forma_pagamento').val('');
}

$('#id_form_criar_ou_editar_financeiro').submit(function(e){
    EasyLoading.show({
        type: EasyLoading.TYPE["BALL_PULSE"],
        text: 'Salvando Serviço...',
        timeout: null,
    });

    $("#button_salvar_financeiro").prop("disabled",true);
    e.preventDefault();
    $.post("/financeiro/", $(this).serialize(), function(data){
        if (data.status){
            window.location.reload()
        }else{
            EasyLoading.hide();
            $("#button_salvar_financeiro").prop("disabled",false);
            $.each(data.msg, (index, erro) => {
                toastr.error(erro)
            })
        }
    }, 'json');
});

$('#id_form_excluir_financeiro').submit(function(e){
    EasyLoading.show({
        type: EasyLoading.TYPE["BALL_PULSE"],
        text: 'Excluindo o lançamento...',
        timeout: null,
    });

    $("#button_excluir_financeiro").prop("disabled",true);
    e.preventDefault();
    $.post("/financeiro/", $(this).serialize(), function(data){
        if (data.status){
            window.location.reload()
        }else{
            EasyLoading.hide();
            $("#button_excluir_financeiro").prop("disabled",false);
            $.each(data.msg, (index, erro) => {
                toastr.error(erro)
            })
        }
    }, 'json');
});



/*************************************************** Formulários ******************************************************/

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
        "</div>" +
      "</div>" +
    "</div>"
  );

  $container.find(".select2-result-repository__title").text(paciente.text);


  return $container;
}

function formatPacienteSelection (paciente) { return paciente.nomeCompleto || paciente.text; }

$("#procedimentos").on("select2:select", function (e) {
  let ids = $(e.currentTarget).val();
  $.ajax({
        url: "/servico/getValorTotal",
        data: {'ids': ids.toString()},
        dataType: 'json',
        success: function (data) {
            if(data.status){
                $('#valor_servicos').val(data.valor_servicos);
            }else{
                $.each(data.msg, (index, erro) => {
                    toastr.error(erro)
                })
            }
        }
  });
});

$("#procedimentos").on("select2:unselect", function (e) {
  let ids = $(e.currentTarget).val();
  $.ajax({
        url: "/servico/getValorTotal",
        data: {'ids': ids.toString()},
        dataType: 'json',
        success: function (data) {
            if(data.status){
                $('#valor_servicos').val(data.valor_servicos);
            }else{
                alert('Erro ao consultar valores dos servicos');
            }
        }
  });
});

$("#procedimentos").select2({
    theme: 'bootstrap4',
    allowClear: true,
    placeholder: "Selecione os servicos",
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
                                valor_total: servico.valor_total,
                            }
                         })
            };
        },

        cache: true
    },
    function (markup) { return markup; },
    templateResult: formatServico,
    templateSelection: formatServicoSelection
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