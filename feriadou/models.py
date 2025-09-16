from django.db import models
import sys
from dataclasses import dataclass
from django.conf import settings

try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

# Create your models here.

#Local dataclass
@dataclass
class Local():
    Cidade: str
    Estado: str

#Feriado model
class Feriado(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    date = models.DateField()
    local = Local()
    NACIONAL = 'Nacional'
    ESTADUAL = 'Estadual'
    MUNICIPAL = 'Municipal'
    escopo_choices = [
        (NACIONAL, "Nacional"),
        (ESTADUAL, "Estadual"),
        (MUNICIPAL, "Municipal"),
    ]
    escopo = models.CharField(
        null = False,
        choices=escopo_choices,
        default=NACIONAL,
    )

    def __str__(self):
        return f"""
        Nome: {self.name},
        Data: {self.date},
        Escopo: {self.escopo}"
        """
