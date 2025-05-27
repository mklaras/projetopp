from django.contrib import admin
from django.urls import path
from agendamento import views  
from agendamento.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    
    # URLs para Pacientes
    path('pacientes/', views.PacienteListView.as_view(), name='paciente-list'),
    path('pacientes/novo/', views.PacienteCreateView.as_view(), name='paciente-create'),
    path('pacientes/<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='paciente-update'),
    path('pacientes/<int:pk>/excluir/', views.PacienteDeleteView.as_view(), name='paciente-delete'),
    
    # URLs para Médicos
    path('medicos/', views.MedicoListView.as_view(), name='medico-list'),
    path('medicos/novo/', views.MedicoCreateView.as_view(), name='medico-create'),
    path('medicos/<int:pk>/editar/', views.MedicoUpdateView.as_view(), name='medico-update'),
    path('medicos/<int:pk>/excluir/', views.MedicoDeleteView.as_view(), name='medico-delete'),
    
    # URLs para Consultas
    path('consultas/', views.ConsultaListView.as_view(), name='consulta-list'),
    path('consultas/novo/', views.ConsultaCreateView.as_view(), name='consulta-create'),
    path('consultas/<int:pk>/editar/', views.ConsultaUpdateView.as_view(), name='consulta-update'),
    path('consultas/<int:pk>/excluir/', views.ConsultaDeleteView.as_view(), name='consulta-delete'),
    
    # URLs funcionais
    path('medicos/<int:medico_id>/agenda/', views.agenda_medico, name='agenda-medico'),
    path('pacientes/<int:paciente_id>/historico/', views.historico_paciente, name='historico-paciente'),
]