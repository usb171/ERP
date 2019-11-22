$('[data-mask]').inputmask();


$("#id_nav_link_produtos").addClass("active");

/****************************************************** Tabela ********************************************************/
    let table = $("#id_table_produtos").DataTable({

        dom:"<'row be-datatable-header'<'col-sm-6'B><'col-sm-6'f>>" +
            "<'row be-datatable-body'<'col-sm-12'tr>>" +
            "<'row be-datatable-footer'<'col-sm-5'i><'col-sm-7'p>>",

        buttons: [
            {
                text: 'Novo Produto',
                action: function ( e, dt, node, config ) {
                    $('#id_modal_produto_novo_editar h4').text('Novo Produto');
                    $('#id_modal_produto_novo_editar').modal('show');
                    limparform();
                    $("#comando_novo_editar").val(comando);

                },
                className: 'btn btn-success '
            },
            {
                text: 'Editar Produto',
                action: function ( e, dt, node, config ) {
                    let comando = '#editar#'
                    let id = table.rows({selected:true}).data()[0][0]
                    $('#id_modal_produto_novo_editar h4').text('Editar Produto');
                    $('#id_modal_produto_novo_editar').modal('show');
                    $("#comando_novo_editar").val(comando);
                    $("#id_criar_editar").val(id);
                },
                className: 'btn btn-warning',
                enabled: false
            },
            {
                text: 'Excluir Produto',
                action: function ( e, dt, node, config ) {
                    let linha = table.rows({selected:true}).data()[0];
                    let id = linha[0];
                    let nome = linha[1];
                    $('#id_modal_produto_excluir').modal('show');
                    $("#id_excluir").val('');
                    $("#codigo_excluir_produto").text(id);
                    $("#id_produto_selecionado").val(id);
                    $("#nome_excluir_produto").text(nome);
                },
                className: 'btn btn-danger',
                enabled: true
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
        "serverSide": true,
        "ajax": "/produto/buscarProdutos",

        "bLengthChange": false,
        "pageLength": 5,
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
        if(linha){
            let id = linha[0];
            carregarDadosLinhaSelecionada(id);
        }
        table.button(1).enable( selectedRows > 0 );
        table.button(2).enable( selectedRows > 0 );
    });
/****************************************************** Tabela ********************************************************/
    /***************************************** Formulários **********************************************/
    let carregarDadosLinhaSelecionada = (id) =>{
        $.get( "/produto/getDados/", { id: id } )
        .done(function(data) {
            $('#id_modal_produto_novo_editar form').trigger('reset'); // reseta todos os campos do formulário
            data = data.produto;
            $('#id').val(id);
            $('#nome_produto').val(data.nome_produto);
            $('#valor_produto').val(data.valor_produto);
        })
    }
    let limparform = () => {
    $("#nome_produto").val('');
    $("#valor_produto").val('');
}

    $('#id_form_novo_editar').submit(function(e){
        EasyLoading.show({
            type: EasyLoading.TYPE["BALL_PULSE"],
            text: 'Salvando Produto',
            timeout: null,
        });
        $("#button_salvar_produto").prop("disabled",true);
        e.preventDefault();
        $.post("/produto/", $(this).serialize(), function(data){
            console.log(data)
            if (data.status){
                window.location.reload()
            }else{
                $("#button_salvar_paciente").prop("disabled",false);
                $.each(data.msg, (index, erro) => {
                    toastr.error(erro)
                })
            }
        }, 'json');
    });

    $('#id_form_excluir_produto').submit(function(e){
    EasyLoading.show({
        type: EasyLoading.TYPE["BALL_PULSE"],
        text: 'Excluindo Produto...',
        timeout: null,
    });

    $("#button_excluir_produto").prop("disabled",true);
    e.preventDefault();
    $.post("/produto/", $(this).serialize(), function(data){
        if (data.status){
            window.location.reload()
        }else{
            EasyLoading.hide();
            $("#button_excluir_produto").prop("disabled",false);
            $.each(data.msg, (index, erro) => {
                toastr.error(erro)
            })
        }
    }, 'json');
});

/*************************************************** Formulários ***********************************************/
