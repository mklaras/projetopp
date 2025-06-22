from django import forms
from .models import Paciente, Medico, Consulta
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento', 'telefone']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(99) 99999-9999'}),
        }

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome', 'especialidade', 'crm', 'telefone']
        widgets = {
            'telefone': forms.TextInput(attrs={'placeholder': '(99) 99999-9999'}),
        }

class ConsultaForm(forms.ModelForm):
    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    horario = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = Consulta
        fields = ['medico', 'paciente', 'data_hora', 'observacoes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['data'].initial = self.instance.data_hora.date()
            self.fields['horario'].initial = self.instance.data_hora.time()
    
    def save(self, commit=True):
        consulta = super().save(commit=False)
        data = self.cleaned_data['data']
        horario = self.cleaned_data['horario']
        naive_datetime = datetime.combine(data, datetime.strptime(horario, '%H:%M').time())
    
        consulta.data_hora = timezone.make_aware(naive_datetime)
        
        if commit:
            consulta.save()
        return consulta