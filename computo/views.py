from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from .models import Computo, CandidatoEleccion, DetalleComputo, Candidato
from control.models import Mesa, Eleccion, Seccion, Cargo
from .forms import VotosForm
from django.http import Http404
from django.db.models import Count, F, ExpressionWrapper, FloatField, Value, Case, When, Sum, IntegerField
from django.db.models.functions import Coalesce

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

            # Obtén los cargos disponibles para esta elección
            cargos_disponibles = Cargo.objects.filter(candidatoeleccion__eleccion=computo.eleccion).distinct()

            # Usamos la Sección para obtener todas las mesas
            mesas = Mesa.objects.filter(escuela__circuito__seccion=seccion)

            # Calcula el porcentaje de carga para cada mesa
            for mesa in mesas:
                total_candidatos = 0
                total_cargados = 0

                for cargo in cargos_disponibles:
                    candidatos_cargo = CandidatoEleccion.objects.filter(
                        eleccion=computo.eleccion,
                        cargo=cargo
                    )

                    total_candidatos_cargo = candidatos_cargo.count()

                    if total_candidatos_cargo > 0:
                        total_candidatos += total_candidatos_cargo

                        total_cargados_cargo = mesa.detallecomputo_set.filter(
                            computo=computo,
                            candidato_eleccion__in=candidatos_cargo,
                            cantidad_voto__isnull=False
                        ).count()

                        total_cargados += total_cargados_cargo

                if total_candidatos > 0:
                    porcentaje_mesa = (total_cargados / total_candidatos) * 100
                else:
                    porcentaje_mesa = 0

                mesa.porcentaje = porcentaje_mesa

            context['mesas'] = mesas
            context['computo'] = computo
            context['cargos_disponibles'] = cargos_disponibles

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

    def get(self, request, computo_id, mesa_id, cargo_id):
        computo = Computo.objects.get(pk=computo_id)
        candidatos = CandidatoEleccion.objects.filter(eleccion=computo.eleccion, cargo_id=cargo_id)
        cargo = Cargo.objects.get(pk=cargo_id)

        candidatos_con_valor = []

        # Obtén el objeto Mesa de la misma manera que en la vista ComputoMesaListView
        mesa = Mesa.objects.get(pk=mesa_id)

        for candidato in candidatos:
            cantidad_voto = candidato.detallecomputo_set.filter(computo=computo, mesa=mesa).first()
            candidatos_con_valor.append({
                'candidato': candidato.candidato,
                'cantidad_voto': cantidad_voto.cantidad_voto if cantidad_voto else None
            })

        return render(request, self.template_name, {'candidatos': candidatos_con_valor, 'mesa': mesa, 'computo':computo, 'cargo':cargo})


    
    def post(self, request, computo_id, mesa_id, cargo_id):
        computo = Computo.objects.get(pk=computo_id)
        candidatos = CandidatoEleccion.objects.filter(eleccion=computo.eleccion, cargo_id=cargo_id)
        
        for candidato in candidatos:
            nombre_campo = f'cantidad_voto_{candidato.candidato.id}'
            cantidad_voto = request.POST.get(nombre_campo)
            
            # Manejar el caso cuando cantidad_voto es un string vacío
            if cantidad_voto == '':
                cantidad_voto = None
            else:
                try:
                    cantidad_voto = int(cantidad_voto)
                except ValueError:
                    cantidad_voto = None

            # Intentar obtener el primer objeto DetalleComputo para esta combinación
            detalle, created = DetalleComputo.objects.get_or_create(
                computo=computo,
                mesa_id=mesa_id,
                candidato_eleccion=candidato
            )

            # Establecer el valor de cantidad_voto en el objeto DetalleComputo
            detalle.cantidad_voto = cantidad_voto
            detalle.save()

        return redirect('computo_mesa_list', computo_id=computo_id)