from django.contrib import admin
from .models import *

class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nomeCompleto', 'telefone']

admin.site.register(Paciente, PacienteAdmin)
