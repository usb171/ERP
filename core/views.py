from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.conf import settings
import json

from django.shortcuts import render, redirect
from .forms import *

from .funcoes.buscas import *
from .funcoes.conta import *


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

    @login_required(login_url='login')
    def conta(request):
        template_name = "core/paginas/conta.html"
        context = {'conta': Buscas.core_get_conta(request.user), 'sessao': {}}
        if request.method == 'GET':
            return render(request=request, template_name=template_name, context=context)
        if request.method == 'POST':
            return HttpResponse(json.dumps(criarEditarExcluirAlterarDadosAlterarSenha(request)),
                                content_type="application/json")
