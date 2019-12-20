$('[data-mask]').inputmask();

$("#id_nav_link_pacientes").addClass("active");


/****************************************************** Tabela ********************************************************/
let table = $("#id_table_pacientes").DataTable({

    dom:"<'row be-datatable-header'<'col-sm-6'B><'col-sm-6'f>>" +
        "<'row be-datatable-body'<'col-sm-12'tr>>" +
        "<'row be-datatable-footer'<'col-sm-5'i><'col-sm-7'p>>",

    buttons: [
        {
            text: 'Novo Paciente',
            action: function ( e, dt, node, config ) {
                limparform();
                let comando = '#criar#'
                $('#id_modal_paciente_novo_editar h4').text('Novo Paciente');
                $('#id_modal_paciente_novo_editar').modal('show');
                $("#comando_novo_editar").val(comando);
            },
            className: 'btn btn-success'
        },
        {
            text: 'Editar Paciente',
            action: function ( e, dt, node, config ) {
                limparform();
                let comando = '#editar#'
                let id = table.rows({selected:true}).data()[0][0]
                $('#id_modal_paciente_novo_editar h4').text('Editar Paciente');
                $('#id_modal_paciente_novo_editar').modal('show');
                $("#comando_novo_editar").val(comando);
                carregarDadosLinhaSelecionada(id);

            },
            className: 'btn btn-warning',
            enabled: false
        },
        {
            text: 'Excluir Paciente',
            action: function ( e, dt, node, config ) {
                let linha = table.rows({selected:true}).data()[0];
                let id = linha[0];
                let nome = linha[1];
                $('#id_modal_paciente_excluir').modal('show');
                $("#id_excluir").val('');
                $("#codigo_excluir_paciente").text(id);
                $("#id_paciente_selecionado").val(id);
                $("#nome_excluir_paciente").text(nome);
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

    EasyLoading.show({
        type: EasyLoading.TYPE["BALL_PULSE"],
        text: 'Carregando dados...',
        timeout: null,
    });

    $.get( "/paciente/getPaciente/", { id: id } )
    .done(function(data) {
        data = data.paciente;
        $('#id').val(id);
        $('#nomeCompleto').val(data.nomeCompleto);
        $('#whatsapp').val(data.whatsapp);
        $('#telefone').val(data.telefone);
        $('#cidade').val(data.cidade);
        $('#cep').val(data.cep);
        $('#facebook').val(data.facebook);
        $('#instagram').val(data.instagram);
        $('#email').val(data.email);
        $('#email').removeClass("is-invalid");
        $("#id_criar_editar").val(id);
        EasyLoading.hide();
    })
}

let limparform = () => {
    $("#nomeCompleto").val('');
    $("#whatsapp").val('');
    $("#telefone").val('');
    $("#cidade").val('');
    $("#cep").val('');
    $("#facebook").val('');
    $("#instagram").val('');
    $("#email").val('');
}

$('#id_form_criar_ou_editar_paciente').submit(function(e){
    EasyLoading.show({
        type: EasyLoading.TYPE["BALL_PULSE"],
        text: 'Salvando Paciente...',
        timeout: null,
    });
    $("#button_salvar_paciente").prop("disabled",true);
    e.preventDefault();
    $.post("/paciente/", $(this).serialize(), function(data){
        if (data.status){
            window.location.reload()
        }else{
            EasyLoading.hide();
            $("#button_salvar_paciente").prop("disabled",false);
            $("#email").addClass("is-invalid");
            $.each(data.msg, (index, erro) => {
                toastr.error(erro)
            })
        }
    }, 'json');
});

$('#id_form_excluir_paciente').submit(function(e){
    EasyLoading.show({
        type: EasyLoading.TYPE["BALL_PULSE"],
        text: 'Excluindo Paciente...',
        timeout: null,
    });

    $("#button_excluir_paciente").prop("disabled",true);
    e.preventDefault();
    $.post("/paciente/", $(this).serialize(), function(data){
        if (data.status){
            window.location.reload()
        }else{
            EasyLoading.hide();
            $("#button_excluir_paciente").prop("disabled",false);
            $.each(data.msg, (index, erro) => {
                toastr.error(erro)
            })
        }
    }, 'json');
});

/*************************************************** Formulários ******************************************************/