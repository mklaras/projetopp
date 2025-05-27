from django.contrib import admin
from .models import Paciente, Medico, Consulta

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'data_nascimento', 'telefone')
    search_fields = ('nome', 'cpf')

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especialidade', 'crm', 'telefone')
    search_fields = ('nome', 'crm', 'especialidade')

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'data_hora')
    list_filter = ('medico', 'data_hora')
    date_hierarchy = 'data_hora'