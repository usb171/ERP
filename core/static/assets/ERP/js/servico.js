$('[data-mask]').inputmask();

$("#id_nav_treeview_configuracoes").addClass("menu-open");
$("#id_nav_link_servicos").addClass("active");

/****************************************************** Tabela ********************************************************/
let table = $("#id_table_servico").DataTable({

    dom:"<'row be-datatable-header'<'col-sm-6'B><'col-sm-6'f>>" +
        "<'row be-datatable-body'<'col-sm-12'tr>>" +
        "<'row be-datatable-footer'<'col-sm-5'i><'col-sm-7'p>>",

    buttons: [
        {
            text: 'Novo Serviço',
            action: function ( e, dt, node, config ) {
                limparform();
                let comando = '#criar#'
                $('#id_modal_servico_novo_editar h4').text('Novo Serviço');
                $('#id_modal_servico_novo_editar').modal('show');
                $("#comando_novo_editar").val(comando);
            },
            className: 'btn btn-success'
        },
        {
            text: 'Editar Serviço',
            action: function ( e, dt, node, config ) {
                limparform();
                let comando = '#editar#'
                let id = table.rows({selected:true}).data()[0][0]
                $('#id_modal_servico_novo_editar h4').text('Editar Serviço');
                $('#id_modal_servico_novo_editar').modal('show');
                $("#comando_novo_editar").val(comando);
                carregarDadosLinhaSelecionada(id);

            },
            className: 'btn btn-warning',
            enabled: false
        },
        {
            text: 'Excluir Serviço',
            action: function ( e, dt, node, config ) {
                let linha = table.rows({selected:true}).data()[0];
                let id = linha[0];
                let nome = linha[1];
                $('#id_modal_servico_excluir').modal('show');
                $("#id_excluir").val('');
                $("#codigo_excluir_servico").text(id);
                $("#id_servico_selecionado").val(id);
                $("#nome_excluir_servico").text(nome);
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


$("#tempo").keyup(function( event ) {
    if (this.value.length > 3) this.value = this.value.slice(0,3);
    this.value = this.value.replace(/[^0-9]/g, '');
    if(this.value[0] == '0') this.value = parseInt(this.value)
    if(!this.value) this.value = '0'
});

$("#valor_produtos").keyup(function( event ) {
    if (this.value.length > 3) this.value = this.value.slice(0,3);
    this.value = this.value.replace(/[^0-9]/g, '');
    if(this.value[0] == '0') this.value = parseInt(this.value)
    if(!this.value) this.value = '0'
});

$("#valor_mao_obra").keyup(function( event ) {
    if (this.value.length > 3) this.value = this.value.slice(0,3);
    this.value = this.value.replace(/[^0-9]/g, '');
    if(this.value[0] == '0') this.value = parseInt(this.value)
    if(!this.value) this.value = '0'
});

$("#valor_clinica").keyup(function( event ) {
    if (this.value.length > 3) this.value = this.value.slice(0,3);
    this.value = this.value.replace(/[^0-9]/g, '');
    if(this.value[0] == '0') this.value = parseInt(this.value)
    if(!this.value) this.value = '0'
});

$("#valor_total").keyup(function( event ) {
    if (this.value.length > 3) this.value = this.value.slice(0,3);
    this.value = this.value.replace(/[^0-9]/g, '');
    if(this.value[0] == '0') this.value = parseInt(this.value)
    if(!this.value) this.value = '0'
});


let carregarDadosLinhaSelecionada = (id) => {

    EasyLoading.show({
        type: EasyLoading.TYPE["BALL_PULSE"],
        text: 'Carregando dados...',
        timeout: null,
    });

    $.get( "/servico/getDados/", { id: id } )
    .done(function(data) {
        data = data.servico;
        $('#id').val(id);
        $('#nome_servico').val(data.nome_servico);
        $('#valor_servico').val(data.valor_servico);
        $('#tempo_servico').val(data.tempo_servico);
        $("#id_criar_editar").val(id);
        EasyLoading.hide();
    })
}

let limparform = () => {
    $("#nome_servico").val('');
    $("#valor_servico").val('');
    $("#tempo_servico").val('');
}

$('#id_form_criar_ou_editar_servico').submit(function(e){
    EasyLoading.show({
        type: EasyLoading.TYPE["BALL_PULSE"],
        text: 'Salvando Serviço...',
        timeout: null,
    });
    $("#button_salvar_servico").prop("disabled",true);
    e.preventDefault();
    $.post("/servico/", $(this).serialize(), function(data){
        if (data.status){
            window.location.reload()
        }else{
            EasyLoading.hide();
            $("#button_salvar_servico").prop("disabled",false);
            $.each(data.msg, (index, erro) => {
                toastr.error(erro)
            })
        }
    }, 'json');
});

$('#id_form_excluir_servico').submit(function(e){
    EasyLoading.show({
        type: EasyLoading.TYPE["BALL_PULSE"],
        text: 'Excluindo Servico...',
        timeout: null,
    });

    $("#button_excluir_servico").prop("disabled",true);
    e.preventDefault();
    $.post("/servico/", $(this).serialize(), function(data){
        if (data.status){
            window.location.reload()
        }else{
            EasyLoading.hide();
            $("#button_excluir_servico").prop("disabled",false);
            $.each(data.msg, (index, erro) => {
                toastr.error(erro)
            })
        }
    }, 'json');
});

/*************************************************** Formulários ******************************************************/

// Select2 *************************************************************************************************************

$("#produto").on("select2:select", function (e) {
  let ids = $(e.currentTarget).val();
  $.ajax({
        url: "/servico/getValor",
        data: {'ids': ids.toString()},
        dataType: 'json',
        success: function (data) {
            console.log(data)
        }
  });
});


$("#produto").select2({
    theme: 'bootstrap4',
    allowClear: true,
            placeholder: "Selecione os produtos",
    ajax: {
        url: "/produto/getProdutos",
        dataType: 'json',
        delay: 100,
        data: function (params) {
                return {
                    q: params.term,
                };
        },
        processResults:function(data){
            return {
                results: $.map(data.produtos, function (produto) {
                            return {
                                id: produto.id,
                                text: produto.nome_produto,
                                valor: produto.valor_produto,
                            }
                         })
            };
        },
        cache: true
    },
    templateResult: formatProduto,
    templateSelection: formatProdutoSelection
});

function formatProduto (produto) {
  if (produto.loading) {
    return produto.text;
  }

  var $container = $(
    "<div class='select2-result-repository clearfix'>" +
      "<div class='select2-result-repository__meta'>" +
        "<div class='select2-result-repository__title'></div>" +
        "<div class='select2-result-repository__statistics'>" +
          "<div class='select2-result-repository__valor'>R$</div>" +
        "</div>" +
      "</div>" +
    "</div>"
  );

  $container.find(".select2-result-repository__title").text(produto.text);
  $container.find(".select2-result-repository__valor").append("     " +  produto.valor);


  return $container;
}

function formatProdutoSelection (produto) { return produto.nome_produto || produto.text; }