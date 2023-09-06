from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from .models import Computo, CandidatoEleccion, DetalleComputo
from control.models import Mesa, Eleccion, Seccion
from .forms import VotosForm
from django.http import Http404

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
    

class DetalleComputoMesaView(View):
    template_name = 'detalle_computo_mesa.html'

    def get(self, request, computo_id, mesa_id):
        computo = Computo.objects.get(pk=computo_id)
        candidatos = CandidatoEleccion.objects.filter(eleccion=computo.eleccion)

        candidatos_con_valor = []

        for candidato in candidatos:
            cantidad_voto = candidato.detallecomputo_set.filter(computo=computo, mesa_id=mesa_id).first()
            candidatos_con_valor.append({
                'candidato': candidato.candidato,
                'cantidad_voto': cantidad_voto.cantidad_voto if cantidad_voto else None
            })

        return render(request, self.template_name, {'candidatos': candidatos_con_valor, 'mesa': mesa_id})

    
    def post(self, request, computo_id, mesa_id):
        computo = Computo.objects.get(pk=computo_id)
        candidatos = CandidatoEleccion.objects.filter(eleccion=computo.eleccion)
        
        for candidato in candidatos:
            nombre_campo = f'cantidad_voto_{candidato.candidato.id}'
            cantidad_voto = request.POST.get(nombre_campo, 0)
            
            try:
                cantidad_voto = int(cantidad_voto)
            except ValueError:
                cantidad_voto = 0

            detalle, created = DetalleComputo.objects.get_or_create(computo=computo, mesa_id=mesa_id, candidato_eleccion=candidato)
            detalle.cantidad_voto = cantidad_voto
            detalle.save()

        return redirect('computo_mesa_list', computo_id=computo_id)


def detalle_computo_mesa(request, computo_id, mesa_id):
    computo = Computo.objects.get(id=computo_id)
    mesa = Mesa.objects.get(id=mesa_id)

    detalles = DetalleComputo.objects.filter(computo=computo, mesa=mesa)
    candidatos = CandidatoEleccion.objects.filter(eleccion=computo.eleccion).order_by('orden')

    # Creamos un diccionario para almacenar la cantidad de votos por candidato
    votos_por_candidato = {}
    for candidato in candidatos:
        detalle = detalles.filter(candidato_eleccion=candidato).first()
        votos_por_candidato[candidato.id] = detalle.cantidad_voto if detalle else 0

    # Procesar el formulario enviado
    if request.method == 'POST':
        form = VotosForm(request.POST)
        if form.is_valid():
            for candidato in candidatos:
                cantidad_voto = form.cleaned_data[f'votos_{candidato.id}']
                detalle, created = DetalleComputo.objects.get_or_create(
                    computo=computo,
                    mesa=mesa,
                    candidato_eleccion=candidato
                )
                detalle.cantidad_voto = cantidad_voto
                detalle.save()
            return redirect('detalle_computo_mesa', computo_id=computo_id, mesa_id=mesa_id)

    else:
        form = VotosForm(initial=votos_por_candidato)  # Inicializa el formulario con los votos existentes

    context = {
        'computo': computo,
        'mesa': mesa,
        'candidatos': candidatos,
        'votos_por_candidato': votos_por_candidato,
        'form': form,  # Pasa el formulario al contexto
    }

    return render(request, 'detalle_computo_mesa.html', context)