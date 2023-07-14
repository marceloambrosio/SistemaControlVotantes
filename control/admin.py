from django.contrib import admin
from .models import Seccion, Circuito, Escuela, Mesa, Persona, User
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group


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

class GroupAdmin(BaseGroupAdmin):
    pass

class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Circuitos', {'fields': ('circuitos',)}),  # Agrega este campo
    )
    filter_horizontal = ('groups', 'user_permissions', 'circuitos')  # Permite una interfaz más amigable para seleccionar circuitos

admin.site.register(Seccion, SeccionAdmin)
admin.site.register(Circuito, CircuitoAdmin)
admin.site.register(Escuela, EscuelaAdmin)
admin.site.register(Mesa, MesaAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
#admin.site.register(User, BaseUserAdmin)
admin.site.register(Group, GroupAdmin)