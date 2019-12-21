$("#id_nav_treeview_configuracoes").addClass("menu-open");
$("#id_nav_link_conta").addClass("active");

$('#id_form_acesso').submit(function(e){
    $("#id_button_alterar_senha").prop("disabled",true);
    e.preventDefault();
    $.post("/conta", $(this).serialize(), function(data){
        if(data.alterado){
            $('#id_modal').modal('show')
            setTimeout(function(){location.href="/logout"}, 3000);
        }else{
            $("#id_old_password").removeClass("is-invalid").addClass("is-valid");
            $("#id_new_password1").removeClass("is-invalid").addClass("is-valid");
            $("#id_new_password2").removeClass("is-invalid").addClass("is-valid");

            if(data.erros["old_password"] != undefined){
                $.each(data.erros.old_password, (index, erro) => {
                    toastr.error(erro)
                })
                $("#id_old_password").removeClass("is-valid").addClass("is-invalid");
            }
            if(data.erros["new_password1"] != undefined){
                $.each(data.erros.new_password1, (index, erro) => {
                    toastr.error(erro)
                })
                $("#id_new_password1").removeClass("is-valid").addClass("is-invalid");
            }
            if(data.erros["new_password2"] != undefined){
                $.each(data.erros.new_password2, (index, erro) => {
                    toastr.error(erro)
                })
                $("#id_new_password2").removeClass("is-valid").addClass("is-invalid");
            }
        }
    $("#id_button_alterar_senha").prop("disabled",false);
    }, 'json');
});