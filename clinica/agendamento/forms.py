from django import forms
from .models import Paciente, Medico, Consulta
from django.core.exceptions import ValidationError
from django.utils import timezone

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento', 'telefone']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
        
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome', 'especialidade', 'crm', 'telefone']
        
class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'data_hora', 'observacoes']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    def clean_data_hora(self):
        data_hora = self.cleaned_data.get('data-hora')
        if data_hora and data_hora < timezone.now():
            raise ValidationError("Não é possível agendar consultas no passado.")
        return data_hora 