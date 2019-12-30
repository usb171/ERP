$('[data-mask]').inputmask();

$('#valor').inputmask(
    'decimal', {
        'integerDigits': 5,
        'alias': 'numeric',
        'autoGroup': true,
        'digits': 2,
        'digitsOptional': false,
        'allowMinus': false,
        'placeholder': ''
    }
);


$("#id_nav_treeview_configuracoes").addClass("menu-open");
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
                    limparform();
                    let comando = '#criar#'
                    $('#id_modal_produto_novo_editar h4').text('Novo Produto');
                    $('#id_modal_produto_novo_editar').modal('show');
                    $("#comando_novo_editar").val(comando);

                },
                className: 'btn btn-success '
            },
            {
                text: 'Editar Produto',
                action: function ( e, dt, node, config ) {
                    EasyLoading.show({type: EasyLoading.TYPE["BALL_PULSE"],text: 'Carregando dados...', timeout: null});
                    let id = table.rows({selected:true}).data()[0][0]
                    carregarDadosLinhaSelecionada(id)
                    limparform();
                    let comando = '#editar#'
                    $('#id_modal_produto_novo_editar').modal('show');
                    $('#id_modal_produto_novo_editar h4').text('Editar Produto');
                    $("#comando_novo_editar").val(comando);
                    EasyLoading.hide();
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


/**************************************************** Formulários *****************************************************/
    let carregarDadosLinhaSelecionada = (id) =>{
        $.ajax({
                url: "/produto/getProduto/",
                data: {'id': id},
                dataType: 'json',
                success: function (data) {
                    produto = data.produto;
                    status = data.status;
                    if(data.status){
                        $('#id').val(id);
                        $('#nome').val(produto.nome);
                        $('#tipo').val(produto.tipo);
                        $('#quantidade').val(produto.quantidade);
                        $('#valor').val(produto.valor);
                        $("#id_criar_editar").val(id);
                    }else{
                        $.each(data.msg, (index, erro) => {
                            toastr.error(erro)
                        })
                    }
                }
        });

    }

    let limparform = () => {
        $("#nome").val('');
        $("#tipo").val('');
        $("#quantidade").val('');
        $("#valor").val('').removeClass("is-invalid");
    }


    $('#id_form_criar_ou_editar_produto').submit(function(e){
        EasyLoading.show({
            type: EasyLoading.TYPE["BALL_PULSE"],
            text: 'Salvando Produto',
            timeout: null,
        });
        $("#button_salvar_produto").prop("disabled",true);
        e.preventDefault();
        $.post("/produto/", $(this).serialize(), function(data){
            if (data.status){
                window.location.reload()
            }else{
                EasyLoading.hide();
                if(data.erros["valor"] != undefined){
                    $.each(data.erros.valor, (index, erro) => {
                        toastr.error(erro)
                    })
                    $("#valor").removeClass("is-valid").addClass("is-invalid")

                }
                $("#button_salvar_produto").prop("disabled",false);


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

    $("#quantidade").keyup(function( event ) {
        if (this.value.length > 4) this.value = this.value.slice(0,4);
        this.value = this.value.replace(/[^0-9]/g, '');
        if(this.value[0] == '0') this.value = parseInt(this.value)
        if(!this.value) this.value = '0'
    });

/*************************************************** Formulários ***********************************************/

/************************************************** Select2 ***************************************************/
//$("#tipo").select2({
//    theme: 'bootstrap4',
//});