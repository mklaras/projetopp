from django.db import models
from django.core.validators import MinLengthValidator

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
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('medico', 'data_hora')
    
    def __str__(self):
        return f"{self.paciente} com {self.medico} em {self.data_hora}"