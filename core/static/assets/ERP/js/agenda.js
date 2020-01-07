
$("#id_nav_link_agenda").addClass("active");

// Calendar ************************************************************************************************************

let calendarEl = document.getElementById('calendar');
calendar = new FullCalendar.Calendar(calendarEl, {
    plugins: ['interaction', 'dayGrid', 'timeGrid', 'list'],
    themeSystem: 'bootstrap',
    header: {
        left: 'prev,next,today agendar',
        center: 'title',
        right: 'listDay,dayGridMonth'
        //right: 'dayGridMonth,timeGridWeek,timeGridDay,listDay'
    },
    defaultDate: new Date(),
    locale: 'pt',
    buttonIcons: false, // show the prev/next text
    weekNumbers: false,
    navLinks: true, // can click day/week names to navigate views
    businessHours: true, // display business hours
    editable: false,
    selectable: true,
    slotDuration: '00:05:00',
    minTime: '08:00:00',
    maxTime: '18:00:00',
    defaultView: 'list',

    select: function(date, jsEvent, view) {
        console.log('Clicou');
    },
    click: function(info) {
        console.log('Clicou2');
    },
    events: [],
    customButtons: {
        agendar: {
            text: 'Agendar',
            click: function() {
            $('#id_modal_agendar h4').text('Agendamento');
                $("#id_modal_agendar").modal('show');
            }
        }
    },

    eventPositioned: function(event){

    },
});
calendar.render();


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


$("#servicos").select2({
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
        url: "/getUsuarios/",
        dataType: 'json',
        delay: 100,
        data: function (params) {
                return {
                    q: params.term,
                };
        },
        processResults:function(data){
            return {
                results: $.map(data.usuarios, function (usuario) {
                            return {
                                id: usuario.id,
                                text: usuario.username
                            }
                         })
            };
        },
        cache: true
    },
    templateResult: formatUsuario,
    templateSelection: formatUsuarioSelection
});

function formatUsuario (usuario) {
  if (usuario.loading) {
    return usuario.text;
  }

  var $container = $(
    "<div class='select2-result-repository clearfix'>" +
      "<div class='select2-result-repository__meta'>" +
        "<div class='select2-result-repository__title'></div>" +
      "</div>" +
    "</div>"
  );

  $container.find(".select2-result-repository__title").text(usuario.text);


  return $container;
}

function formatUsuarioSelection (usuario) { return usuario.username || usuario.text; }



// Timepicker **********************************************************************************************************

$('#timepicker').datetimepicker({
    format: 'DD/MM/YYYY',
    daysOfWeekDisabled: [0]
})


$("#timepicker").on("change.datetimepicker", function (e) {
    console.log("Oi");
});



