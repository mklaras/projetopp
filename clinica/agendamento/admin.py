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
    
    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()  # Isso vai validar o limite de 12 consultas
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            from django.contrib import messages
            messages.error(request, f"Erro ao salvar consulta: {e}")