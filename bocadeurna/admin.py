from django.contrib import admin
from .models import BocaDeUrna, Cargo, Partido, Candidato, DetalleBocaDeUrna

# Register your models here.

class BocaDeUrnaAdmin(admin.ModelAdmin):
    search_fields = ('circuito'),
    ordering = ['fecha']

class CargoAdmin(admin.ModelAdmin):
    search_fields = ('titulo'),
    ordering = ['titulo']

class PartidoAdmin(admin.ModelAdmin):
    search_fields = ('nombre','lista'),
    ordering = ['nombre']

class CandidatoAdmin(admin.ModelAdmin):
    search_fields = ('apellido','nombre'),
    ordering = ['apellido','nombre']

class DetalleBocaDeUrnaAdmin(admin.ModelAdmin):
    search_fields = ('boca_de_urna'),
    ordering = ['boca_de_urna']


admin.site.register(BocaDeUrna, BocaDeUrnaAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Partido, PartidoAdmin)
admin.site.register(Candidato, CandidatoAdmin)
admin.site.register(DetalleBocaDeUrna, DetalleBocaDeUrnaAdmin)