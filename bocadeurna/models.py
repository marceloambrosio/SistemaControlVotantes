from django.db import models
from control.models import Circuito

# Create your models here.

class BocaDeUrna(models.Model):
    fecha = models.DateField()
    circuito = models.ForeignKey(Circuito, on_delete=models.CASCADE)

    def __str__(self):
        return self.circuito.localidad + " (" + str(self.fecha) + ")"

class Cargo(models.Model):
    titulo = models.CharField()

    def __str__(self):
        return self.titulo

class Partido(models.Model):
    lista = models.CharField()
    nombre = models.CharField()

    def __str__(self):
        return str(self.lista).zfill(2) + " - " + self.nombre

class Candidato(models.Model):
    nombre = models.CharField()
    apellido = models.CharField()
    circuito = models.ForeignKey(Circuito, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    color = models.CharField(default='#000000', max_length=7)

    def __str__(self):
        return self.circuito.localidad + " - " + self.cargo.titulo + " - " + self.apellido + ", " + self.nombre + " (" + self.partido.nombre + ")"

class DetalleBocaDeUrna(models.Model):
    # Definimos las opciones para el campo 'edad'
    OPCIONES_EDAD = (
        ('16-21', '16 a 21 años'),
        ('22-30', '22 a 30 años'),
        ('30-40', '30 a 40 años'),
        ('50-65', '50 a 65 años'),
        ('65+', '65 o más años'),
    )

    edad = models.CharField(max_length=6, choices=OPCIONES_EDAD)
    boca_de_urna = models.ForeignKey(BocaDeUrna, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)

    def __str__(self):
        return self.boca_de_urna.circuito.localidad + " - " + str(self.edad) + " - " + self.candidato.apellido + ", " + self.candidato.nombre + " (" + self.candidato.partido.nombre + ")"
