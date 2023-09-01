from django.contrib import admin
from .models import BocaDeUrna, DetalleBocaDeUrna

# Register your models here.

class BocaDeUrnaAdmin(admin.ModelAdmin):
    search_fields = ('eleccion'),
    ordering = ['eleccion']

class DetalleBocaDeUrnaAdmin(admin.ModelAdmin):
    search_fields = ('boca_de_urna'),
    ordering = ['boca_de_urna']


admin.site.register(BocaDeUrna, BocaDeUrnaAdmin)
admin.site.register(DetalleBocaDeUrna, DetalleBocaDeUrnaAdmin)