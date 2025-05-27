from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Paciente, Medico, Consulta
from .forms import PacienteForm, MedicoForm, ConsultaForm

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

class PacienteUpdateView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'agendamento/paciente_form.html'
    success_url = reverse_lazy('paciente-list')

class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'agendamento/paciente_confirm_delete.html'
    success_url = reverse_lazy('paciente-list')

# Views para Médico
class MedicoListView(ListView):
    model = Medico
    template_name = 'agendamento/medico_list.html'

class MedicoCreateView(CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'agendamento/medico_form.html'
    success_url = reverse_lazy('medico-list')

class MedicoUpdateView(UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'agendamento/medico_form.html'
    success_url = reverse_lazy('medico-list')

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

class ConsultaUpdateView(UpdateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'agendamento/consulta_form.html'
    success_url = reverse_lazy('consulta-list')

class ConsultaDeleteView(DeleteView):
    model = Consulta
    template_name = 'agendamento/consulta_confirm_delete.html'
    success_url = reverse_lazy('consulta-list')

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