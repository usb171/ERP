from django.urls import path
from .views import *

urlpatterns = [
    path('', AgendaView.agenda, name='agenda'),
]