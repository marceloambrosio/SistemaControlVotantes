from django.db import models
from control.models import Circuito, Mesa, Eleccion, Cargo

# Create your models here.

class Partido(models.Model):
    lista = models.CharField()
    nombre = models.CharField()

    def __str__(self):
        return str(self.lista).zfill(2) + " - " + self.nombre

class Candidato(models.Model):
    nombre = models.CharField()
    apellido = models.CharField()
    color = models.CharField(default='#000000', max_length=7)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)

    def __str__(self):
        #return self.circuito.localidad + " - " + self.cargo.titulo + " - " + self.apellido + ", " + self.nombre + " (" + self.partido.nombre + ")"
        return self.apellido + " " + self.nombre

class CandidatoEleccion(models.Model):
    eleccion = models.ForeignKey(Eleccion, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField()

    @classmethod
    def get_available_candidates(cls, circuito, tipo_eleccion):
        return cls.objects.filter(
            candidato__circuito=circuito,
            candidato__cargo__tipo_eleccion=tipo_eleccion
        )

    def __str__(self):
        return self.eleccion.circuito.localidad + " - " + self.candidato.apellido + " " + self.candidato.nombre + " - " + self.cargo.titulo + " (Orden: " + str(self.orden) + ")"

class Computo(models.Model):
    fecha = models.DateField()
    eleccion = models.ForeignKey(Eleccion, on_delete=models.CASCADE)

    def __str__(self):
        return self.eleccion.circuito.localidad + " - " + self.eleccion.tipo_eleccion.nombre + " - " + str(self.fecha.year)

class DetalleComputo(models.Model):
    computo = models.ForeignKey(Computo, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    candidato_eleccion = models.ForeignKey(CandidatoEleccion, on_delete=models.CASCADE)
    cantidad_voto = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.computo.eleccion.circuito.localidad + " (" + self.computo.eleccion.tipo_eleccion.nombre + ") - Mesa Nº " + str(self.mesa.num_mesa) + " - " + self.candidato_eleccion.candidato.nombre + " " + self.candidato_eleccion.candidato.apellido + " - " + str(self.cantidad_voto) + " votos"