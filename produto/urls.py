from django.urls import path
from .views import *

urlpatterns = [
    path('', Cadastro.produtoView, name='cadastroProduto'),

]