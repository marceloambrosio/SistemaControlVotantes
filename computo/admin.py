from django.contrib import admin
from .models import Candidato, Partido, CandidatoEleccion, Computo, DetalleComputo

# Register your models here.

class PartidoAdmin(admin.ModelAdmin):
    search_fields = ('nombre','lista'),
    ordering = ['nombre']

class CandidatoAdmin(admin.ModelAdmin):
    search_fields = ('apellido','nombre'),
    ordering = ['apellido','nombre']

class CandidatoEleccionAdmin(admin.ModelAdmin):
    search_fields = ('eleccion','candidato'),
    ordering = ['eleccion','orden','candidato']

class ComputoAdmin(admin.ModelAdmin):
    search_fields = ('fecha','eleccion'),
    ordering = ['fecha','eleccion']

class DetalleComputoAdmin(admin.ModelAdmin):
    search_fields = ('computo','mesa','candidato_eleccion'),
    ordering = ['computo','mesa']

admin.site.register(Partido, PartidoAdmin)
admin.site.register(Candidato, CandidatoAdmin)
admin.site.register(CandidatoEleccion, CandidatoEleccionAdmin)
admin.site.register(Computo, ComputoAdmin)
admin.site.register(DetalleComputo, DetalleComputoAdmin)