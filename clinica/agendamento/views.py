from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Paciente, Medico, Consulta
from .forms import PacienteForm, MedicoForm, ConsultaForm
from django.contrib import messages
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

class HomeView(TemplateView):
    template_name = 'agendamento/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ultimas_consultas'] = Consulta.objects.all().order_by('-data_hora')[:5]
        return context

class PacienteListView(ListView):
    model = Paciente
    template_name = 'agendamento/paciente_list.html'

class PacienteCreateView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'agendamento/paciente_form.html'
    success_url = reverse_lazy('paciente-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Registro salvo com sucesso!')
        return super().form_valid(form)
    

class PacienteUpdateView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'agendamento/paciente_form.html'
    success_url = reverse_lazy('paciente-list')

    def form_valid(self, form):
        messages.success(self.request, 'Registro salvo com sucesso!')
        return super().form_valid(form)
    
class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'agendamento/paciente_confirm_delete.html'
    success_url = reverse_lazy('paciente-list')

# Views para Médico
class MedicoListView(ListView):
    model = Medico
    template_name = 'agendamento/medico_list.html'
    context_object_name = 'medicos'
    ordering = ['nome']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Médicos no contexto:", context['object_list'])  # Verifique no console
        return context

class MedicoCreateView(CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'agendamento/medico_form.html'
    success_url = reverse_lazy('medico-list')
    def form_valid(self, form):
        messages.success(self.request, 'Registro salvo com sucesso!')
        return super().form_valid(form)
    

class MedicoUpdateView(UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'agendamento/medico_form.html'
    success_url = reverse_lazy('medico-list')

    def form_valid(self, form):
        messages.success(self.request, 'Registro salvo com sucesso!')
        return super().form_valid(form)
    
class MedicoDeleteView(DeleteView):
    model = Medico
    template_name = 'agendamento/medico_confirm_delete.html'
    success_url = reverse_lazy('medico-list')

# Views para Consulta
class ConsultaListView(ListView):
    model = Consulta
    template_name = 'agendamento/consulta_list.html'

class ConsultaCreateView(CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'agendamento/consulta_form.html'
    success_url = reverse_lazy('consulta-list')

    def form_valid(self, form):
        messages.success(self.request, 'Registro salvo com sucesso!')
        return super().form_valid(form)
    
class ConsultaUpdateView(UpdateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'agendamento/consulta_form.html'
    success_url = reverse_lazy('consulta-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Registro salvo com sucesso!')
        return super().form_valid(form)

class ConsultaDeleteView(DeleteView):
    model = Consulta
    template_name = 'agendamento/consulta_confirm_delete.html'
    success_url = reverse_lazy('consulta-list')

class ConsultaHorariosView(TemplateView):
    login_url = '/admin/login/'
    template_name = 'agendamento/consulta_horarios.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medicos'] = Medico.objects.all().order_by('nome')
        return context

# Views funcionais
def agenda_medico(request, medico_id):
    from django.utils import timezone
    medico = Medico.objects.get(pk=medico_id)
    hoje = timezone.now().date()
    consultas = Consulta.objects.filter(
        medico=medico,
        data_hora__date=hoje
    ).order_by('data_hora')
    return render(request, 'agendamento/agenda_medico.html', {
        'medico': medico,
        'consultas': consultas,
        'data': hoje
    })

def historico_paciente(request, paciente_id):
    paciente = Paciente.objects.get(pk=paciente_id)
    consultas = Consulta.objects.filter(
        paciente=paciente
    ).order_by('-data_hora')
    return render(request, 'agendamento/historico_paciente.html', {
        'paciente': paciente,
        'consultas': consultas
    })
    
def horarios_disponiveis(request, medico_id, data):
    try:
        medico = Medico.objects.get(pk=medico_id)
        data_consulta = datetime.strptime(data, '%Y-%m-%d').date()
        
        # Horário de funcionamento (9h às 18h)
        horarios = []
        hora_atual = datetime.combine(data_consulta, datetime.min.time()) + timedelta(hours=9)
        fim_expediente = datetime.combine(data_consulta, datetime.min.time()) + timedelta(hours=18)
        
        # Consultas já agendadas
        consultas = Consulta.objects.filter(
            medico=medico,
            data_hora__date=data_consulta
        ).values_list('data_hora', flat=True)
        
        # Gera horários disponíveis
        while hora_atual < fim_expediente:
            if hora_atual not in consultas:
                horarios.append(hora_atual.strftime('%H:%M'))
            hora_atual += timedelta(minutes=30)  # Intervalo de 30 minutos
        
        return JsonResponse({'horarios': horarios})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)