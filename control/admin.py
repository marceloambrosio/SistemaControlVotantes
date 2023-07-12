from django.contrib import admin
from .models import Seccion, Circuito, Escuela, Mesa, Persona
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class SeccionAdmin(admin.ModelAdmin):
    search_fields = ('num_seccion','departamento'),
    ordering = ['departamento']

class CircuitoAdmin(admin.ModelAdmin):
    search_fields = ('localidad','num_circuito'),
    ordering = ['localidad']

class EscuelaAdmin(admin.ModelAdmin):
    ordering = ['nombre']

class MesaAdmin(admin.ModelAdmin):
    ordering = ['num_mesa']

class PersonaAdmin(admin.ModelAdmin):
    search_fields = ('apellido','nombre','dni'),
    ordering = ['apellido','nombre','clase']

class PersonaAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Seccion, SeccionAdmin)
admin.site.register(Circuito, CircuitoAdmin)
admin.site.register(Escuela, EscuelaAdmin)
admin.site.register(Mesa, MesaAdmin)
admin.site.register(Persona, PersonaAdmin)