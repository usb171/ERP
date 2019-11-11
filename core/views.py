from django.shortcuts import render

class CoreView():

    def index(request):
        template_name = "core/paginas/index.html"
        context = {}

        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
