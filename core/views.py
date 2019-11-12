from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

from django.shortcuts import render, redirect
from .forms import *

class CoreView():

    @login_required(login_url='login')
    def index(request):
        template_name = "core/paginas/index.html"
        context = {}

        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return render(request=request, template_name=template_name, context=context)

    def login(request):
        template_name = "core/paginas/login.html"
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context={})
        if request.method == 'POST':
            conta = FormConta(request.POST).login(request)
            if conta['logado']:
                return redirect('index')
            else:
                return render(request=request, template_name=template_name, context=conta)

    def logout(request):
        auth_logout(request)
        return redirect('login')
