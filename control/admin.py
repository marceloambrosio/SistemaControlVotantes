from django.contrib import admin
from .models import Seccion, Circuito, Escuela, Mesa, Persona, User, Eleccion, TipoEleccion, Cargo
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group



def reiniciar_votos_circuito(modeladmin, request, queryset):
    for circuito in queryset:
        personas_en_circuito = Persona.objects.filter(mesa__escuela__circuito=circuito)
        personas_en_circuito.update(voto=False)
reiniciar_votos_circuito.short_description = "Reiniciar votos para todas las personas en este circuito"

def reiniciar_votos_mesa(modeladmin, request, queryset):
    for mesa in queryset:
        personas_en_mesa = mesa.persona_set.all()
        personas_en_mesa.update(voto=False)
reiniciar_votos_mesa.short_description = "Reiniciar votos para todas las personas en esta mesa"




# Register your models here.

class SeccionAdmin(admin.ModelAdmin):
    search_fields = ('num_seccion','departamento'),
    ordering = ['departamento']

class CircuitoAdmin(admin.ModelAdmin):
    search_fields = ('localidad','num_circuito'),
    ordering = ['localidad']
    actions = [reiniciar_votos_circuito] 

class EscuelaAdmin(admin.ModelAdmin):
    ordering = ['nombre']

class EscuelaAdmin(ImportExportModelAdmin):
    pass

class MesaAdmin(admin.ModelAdmin):
    ordering = ['num_mesa']
    actions = [reiniciar_votos_mesa]

class MesaAdmin(ImportExportModelAdmin):
    pass

class PersonaAdmin(admin.ModelAdmin):
    search_fields = ('apellido','nombre','dni'),
    ordering = ['apellido','nombre','clase']

class PersonaAdmin(ImportExportModelAdmin):
    pass

class GroupAdmin(BaseGroupAdmin):
    pass

class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Circuitos', {'fields': ('circuitos',)}),  # Agrega este campo
        ('Elección', {'fields': ('eleccion',)}),
    )
    filter_horizontal = ('groups', 'user_permissions', 'circuitos')  # Permite una interfaz más amigable para seleccionar circuitos

class CargoAdmin(admin.ModelAdmin):
    search_fields = ('titulo'),
    ordering = ['titulo']

class TipoEleccionAdmin(admin.ModelAdmin):
    search_fields = ('nombre'),
    ordering = ['nombre','cargo']

class EleccionAdmin(admin.ModelAdmin):
    search_fields = ('fecha','circuito','tipo_eleccion'),
    ordering = ['circuito','tipo_eleccion','fecha']

admin.site.register(Seccion, SeccionAdmin)
admin.site.register(Circuito, CircuitoAdmin)
admin.site.register(Escuela, EscuelaAdmin)
admin.site.register(Mesa, MesaAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
#admin.site.register(User, BaseUserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(TipoEleccion, TipoEleccionAdmin)
admin.site.register(Eleccion, EleccionAdmin)