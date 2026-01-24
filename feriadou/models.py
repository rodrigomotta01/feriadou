from django.db import models
import sys
from dataclasses import dataclass

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
    day = models.PositiveIntegerField()
    month = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 13)])
    local = Local(Cidade='', Estado='')
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
        """Display as MM/DD for templates"""
        return f"{self.day:02d}/{self.month:02d}"
