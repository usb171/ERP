from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class AgendaView():

    @login_required(login_url='login')
    def agenda(request):
        template_name = "agenda/paginas/agenda.html"
        context = {'agenda': []}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return None