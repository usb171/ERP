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


$("#id_nav_treeview_configuracoes_despesa").addClass("menu-open");
$("#id_nav_link_despesa").addClass("active");

/****************************************************** Tabela ********************************************************/
let table = $("#id_table_despesa").DataTable({

    dom:"<'row be-datatable-header'<'col-sm-6'B><'col-sm-6'f>>" +
        "<'row be-datatable-body'<'col-sm-12'tr>>" +
        "<'row be-datatable-footer'<'col-sm-5'i><'col-sm-7'p>>",

    buttons: [
        {
            text: 'Novo',
            action: function ( e, dt, node, config ) {
                limparform();
                let comando = '#criar#'
                $('#id_modal_despesa_novo_editar').modal('show');
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
                $('#id_modal_despesa_novo_editar').modal('show');
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
                $('#id_modal_despesa_excluir').modal('show');
                $("#id_excluir").val('');
                $("#codigo_excluir_despesa").text(id);
                $("#id_despesa_selecionado").val(id);
                $("#nome_excluir_despesa").text(nome);
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
        url: "/financeiro/getDadosDespesa/",
        data: {'id': id},
        dataType: 'json',
        success: function (data) {
            despesa = data.despesa;
            status = data.status;
            if(data.status){
//                $('#id').val(id);
//                $('#valor_servicos').val(receita.valor_apagar);
//                $('#forma_pagamento').val(receita.forma_pagamento);
//                $("#id_criar_editar").val(id);
//                $procedimentos = $('#procedimentos');
//                $.each(receita.procedimentos, (index, servico) => {
//                    $procedimentos.append(new Option(servico.nome, servico.id, true, true)).trigger('change');
//                })
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

$('#id_form_criar_ou_editar_despesa').submit(function(e){
    EasyLoading.show({
        type: EasyLoading.TYPE["BALL_PULSE"],
        text: 'Salvando a Despesa...',
        timeout: null,
    });

    $("#button_salvar_despesa").prop("disabled",true);
    e.preventDefault();
    $.post("/financeiro/despesa/", $(this).serialize(), function(data){
        if (data.status){
            window.location.reload()
        }else{
            EasyLoading.hide();
            $("#button_salvar_despesa").prop("disabled",false);
            $.each(data.msg, (index, erro) => {
                toastr.error(erro)
            })
        }
    }, 'json');
});

$('#id_form_excluir_despesa').submit(function(e){
    EasyLoading.show({
        type: EasyLoading.TYPE["BALL_PULSE"],
        text: 'Excluindo o lançamento...',
        timeout: null,
    });

    $("#button_excluir_despesa").prop("disabled",true);
    e.preventDefault();
    $.post("/financeiro/despesa/", $(this).serialize(), function(data){
        if (data.status){
            window.location.reload()
        }else{
            EasyLoading.hide();
            $("#button_excluir_despesa").prop("disabled",false);
            $.each(data.msg, (index, erro) => {
                toastr.error(erro)
            })
        }
    }, 'json');
});



/*************************************************** Formulários ******************************************************/

// Select2 *************************************************************************************************************
$("#categoria").select2({
    theme: 'bootstrap4',
    allowClear: true,
    placeholder: "Selecione o tipo",
    ajax: {
        url: "/financeiro/getCategorias",
        dataType: 'json',
        delay: 100,
        data: function (params) {
                return {
                    q: params.term,
                };
        },
        processResults:function(data){
            return {
                results: $.map(data.categorias, function (categoria) {
                            return {
                                id: categoria.id,
                                text: categoria.descricao,
                            }
                         })
            };
        },
        cache: true
    },
    function (markup) { return markup; },
    templateResult: formatCategoria,
    templateSelection: formatCategoriaSelection
});

function formatCategoria (categoria) {
  if (categoria.loading) {
    return categoria.text;
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

  $container.find(".select2-result-repository__title").text(categoria.text);


  return $container;
}

function formatCategoriaSelection (categoria) { return categoria.descricao || categoria.text; }
//
//$("#procedimentos").on("select2:select", function (e) {
//  let ids = $(e.currentTarget).val();
//  $.ajax({
//        url: "/servico/getValorTotal",
//        data: {'ids': ids.toString()},
//        dataType: 'json',
//        success: function (data) {
//            if(data.status){
//                $('#valor_servicos').val(data.valor_servicos);
//            }else{
//                $.each(data.msg, (index, erro) => {
//                    toastr.error(erro)
//                })
//            }
//        }
//  });
//});
//
//$("#procedimentos").on("select2:unselect", function (e) {
//  let ids = $(e.currentTarget).val();
//  $.ajax({
//        url: "/servico/getValorTotal",
//        data: {'ids': ids.toString()},
//        dataType: 'json',
//        success: function (data) {
//            if(data.status){
//                $('#valor_servicos').val(data.valor_servicos);
//            }else{
//                alert('Erro ao consultar valores dos servicos');
//            }
//        }
//  });
//});
//
//$("#procedimentos").select2({
//    theme: 'bootstrap4',
//    allowClear: true,
//    placeholder: "Selecione os servicos",
//    ajax: {
//        url: "/servico/getServicos",
//        dataType: 'json',
//        delay: 100,
//        data: function (params) {
//                return {
//                    q: params.term,
//                };
//        },
//        processResults:function(data){
//            return {
//                results: $.map(data.servicos, function (servico) {
//                            return {
//                                id: servico.id,
//                                text: servico.nome,
//                                valor_total: servico.valor_total,
//                            }
//                         })
//            };
//        },
//
//        cache: true
//    },
//    function (markup) { return markup; },
//    templateResult: formatServico,
//    templateSelection: formatServicoSelection
//});
//
//function formatServico (servico) {
//  if (servico.loading) {
//    return servico.text;
//  }
//
//  var $container = $(
//    "<div class='select2-result-repository clearfix'>" +
//      "<div class='select2-result-repository__meta'>" +
//        "<div class='select2-result-repository__title'></div>" +
//        "<div class='select2-result-repository__statistics'>" +
//          "<div class='select2-result-repository__valor_total'>R$ </div>" +
//        "</div>" +
//      "</div>" +
//    "</div>"
//  );
//
//  $container.find(".select2-result-repository__title").text(servico.text);
//  $container.find(".select2-result-repository__valor_total").append("     " +  servico.valor_total);
//
//
//  return $container;
//}
//
//function formatServicoSelection (servico) { return servico.nome || servico.text; }