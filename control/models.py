from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Seccion(models.Model):
    num_seccion = models.IntegerField(primary_key=True)
    departamento = models.CharField()

    def __str__(self):
        return str(self.num_seccion).zfill(2) + " - " + self.departamento

class Circuito(models.Model):
    num_circuito = models.IntegerField(primary_key=True)
    localidad = models.CharField(max_length=100)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    
    def calcular_porcentaje_votos_circuito(self):
        total_personas = self.persona_set.count()
        total_votos = self.persona_set.filter(voto=True).count()

        if total_personas > 0:
            porcentaje_votos = (total_votos / total_personas) * 100
            return round(porcentaje_votos, 2)
        else:
            return 0

    def __str__(self):
        return str(self.num_circuito).zfill(4) + " - " + self.localidad

class Escuela(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    circuito = models.ForeignKey(Circuito, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre + " (" + self.direccion + ") - " + self.circuito.localidad + " (" + self.circuito.seccion.departamento + ")"
    
class Mesa(models.Model):
    num_mesa = models.IntegerField(primary_key=True)
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE)

    def __str__(self):
        return "Mesa Nº " + str(self.num_mesa).zfill(4) + " - " + self.escuela.circuito.localidad
    
    def calcular_cantidad_personas(self):
        return self.persona_set.count()

class Persona(models.Model):
    id = models.AutoField(primary_key=True)
    num_orden = models.IntegerField()
    dni = models.IntegerField()
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    clase = models.IntegerField()
    domicilio = models.CharField(max_length=100)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    voto = models.BooleanField(default=False)

    class Meta:
        unique_together = ('dni', 'apellido', 'nombre','num_orden')

    def __str__(self):
        return str(self.num_orden).zfill(3) + " - " + self.apellido + ", " + self.nombre + " - DNI: " + str(self.dni) + " - Mesa Nº " + str(self.mesa.num_mesa).zfill(4) + " - " + self.mesa.escuela.circuito.localidad
    
class User(AbstractUser):
    circuitos = models.ManyToManyField(Circuito, blank=True)

    def __str__(self):
        return self.username