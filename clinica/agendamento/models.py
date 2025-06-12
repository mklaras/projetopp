from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True, validators=[MinLengthValidator(11)])
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nome

class Medico(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=50)
    crm = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.nome} ({self.especialidade})"

class Consulta(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    observacoes = models.TextField(blank=True, null=True)
    
    def clean(self):
        from django.utils import timezone
        
        # Verifica se a data/hora está no passado
        if self.data_hora and self.data_hora < timezone.now():
            raise ValidationError("Não é possível agendar consultas no passado.")
        
        # Verifica conflito de horário
        if self.medico and self.data_hora:
            # Verifica se já existe consulta no mesmo horário
            conflitos = Consulta.objects.filter(
                medico=self.medico,
                data_hora=self.data_hora
            ).exclude(pk=self.pk).exists()
            
            if conflitos:
                raise ValidationError("O médico já possui uma consulta neste horário.")
            
            # Verifica limite de 12 consultas por dia
            data_consulta = self.data_hora.date()
            consultas_dia = Consulta.objects.filter(
                medico=self.medico,
                data_hora__date=data_consulta
            ).exclude(pk=self.pk).count()
            
            if consultas_dia >= 12:
                raise ValidationError("Este médico já atingiu o limite de 12 consultas neste dia.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ('medico', 'data_hora')
    
    def __str__(self):
        return f"{self.paciente} com {self.medico} em {self.data_hora}"