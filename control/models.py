from django.db import models

# Create your models here.

class Seccion(models.Model):
    num_seccion = models.IntegerField()
    departamento = models.CharField()

    def __str__(self):
        return self.num_seccion + " - " + self.departamento

class Circuito(models.Model):
    num_circuito = models.IntegerField()
    localidad = models.CharField(max_length=100)
    seccion = models.ForeignKey(Seccion, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.num_circuito + " - " + self.seccion

class Escuela(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre + " (" + self.direccion + ")"
    
class Mesa(models.Model):
    num_mesa = models.IntegerField()
    escuela = models.ForeignKey(Escuela, on_delete=models.PROTECT)
    circuito = models.ForeignKey(Circuito, on_delete=models.PROTECT)

    def __str__(self):
        return "Mesa Nº " + self.num_mesa

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.IntegerField()
    domiculio = models.CharField(max_length=100)
    clase = models.IntegerField()

    def __str__(self):
        return self.apellido + ", " + self.nombre + " - DNI: " + str(self.dni)

class PadronMesa(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT)
    num_orden = models.IntegerField()
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)

    def __str__(self):
        return self.num_orden + " - " + self.persona.apellido + self.persona.nombre + " - " + self.persona.dni