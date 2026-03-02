from django.db import models
import sys
from django.contrib.auth.models import User
from django.conf import settings

try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

# Create your models here.

#Feriado model
class Feriado(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    day = models.PositiveIntegerField()
    month = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 13)])
    estado = models.CharField(max_length=50, null=True, blank=True)
    municipio = models.CharField(max_length=50, null=True, blank=True)
    NACIONAL = 'Nacional'
    ESTADUAL = 'Estadual'
    MUNICIPAL = 'Municipal'
    escopo_choices = [
        (NACIONAL, "Nacional"),
        (ESTADUAL, "Estadual"),
        (MUNICIPAL, "Municipal"),
    ]
    escopo = models.CharField(
        max_length = 20,
        null = False,
        choices = escopo_choices,
        default = NACIONAL,
    )

    def __str__(self):
        return f"{self.name} - {self.day:02d}/{self.month:02d} ({self.escopo})"
    
    @property
    def date_display(self):
        return f"{self.day:02d}/{self.month:02d}"

class Usuario(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    #estado =
    #cidade =

    def __str__(self):
        return self.user.get_full_name()
        
class Solicitacao(models.Model):
    name = models.CharField(max_length=100)
    day = models.PositiveIntegerField()
    month = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 13)])
    estado = models.CharField(max_length=50, null=True, blank=True)
    municipio = models.CharField(max_length=50, null=True, blank=True)
    escopo = models.CharField(max_length=50, choices=Feriado.escopo_choices, default=Feriado.NACIONAL)
    PENDENTE = 'Pendente'
    APROVADA = 'Aprovada'
    REJEITADA = 'Rejeitada'
    status_choices = [
        (PENDENTE, 'Pendente'),
        (APROVADA, 'Aprovada'),
        (REJEITADA, 'Rejeitada')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default=PENDENTE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.escopo}"

