from django.contrib import admin
from .models import *


class AgendaAdmin(admin.ModelAdmin):
    list_display = ['status', 'data', 'hora', 'paciente', 'profissional']


admin.site.register(Agenda, AgendaAdmin)
