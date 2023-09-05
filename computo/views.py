from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Computo, CandidatoEleccion
from control.models import Mesa, Eleccion, Seccion

# Create your views here.

class ComputoMesaListView(ListView):
    model = Computo
    template_name = 'computo_mesa_list.html'
    context_object_name = 'computos'

    def get_queryset(self):
        computo_id = self.kwargs['computo_id']
        return Computo.objects.filter(id=computo_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        computo = context['computos'][0]  # Obtenemos el primer objeto de la lista

        # Usamos la relación Eleccion para obtener la Seccion
        seccion = computo.eleccion.circuito.seccion

        # Usamos la Seccion para obtener todas las mesas
        mesas = Mesa.objects.filter(escuela__circuito__seccion=seccion)
        context['mesas'] = mesas

        return context
    
class CandidatoEleccionListView(ListView):
    model = CandidatoEleccion
    template_name = 'candidato_eleccion_list.html'
    context_object_name = 'candidatos_eleccion'

    def get_queryset(self):
        computo_id = self.kwargs['computo_id']
        mesa_id = self.kwargs['mesa_id']

        return CandidatoEleccion.objects.filter(
            eleccion__circuito__escuela__mesa__id=mesa_id,
            eleccion__computo__id=computo_id
        ).order_by('orden')