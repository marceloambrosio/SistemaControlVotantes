from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from .models import Computo, CandidatoEleccion, DetalleComputo, Candidato
from control.models import Mesa, Eleccion, Seccion, Cargo
from .forms import VotosForm
from django.http import Http404
from django.db.models import Count, F, ExpressionWrapper, FloatField, Value, Case, When, Sum, IntegerField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML

# Create your views here.

class CircuitosHabilitadosView(View):
    def get(self, request):
        circuitos = request.user.circuitos.all()
        computo = Computo.objects.filter(eleccion__circuito__in=circuitos).first()  # Obtén el primer objeto Computo (o ajusta la lógica según tus necesidades)

        if computo:
            computo_id = computo.id
        else:
            computo_id = None  # O proporciona un valor predeterminado en caso de que no haya un objeto Computo válido

        context = {'circuitos': circuitos, 'computo_id': computo_id}
        return render(request, 'circuito_habilitado.html', context)



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
            cargos_disponibles = Cargo.objects.filter(candidatoeleccion__eleccion=computo.eleccion).distinct().order_by('orden_cargo')


            # Usamos la Sección para obtener todas las mesas
            mesas = Mesa.objects.filter(escuela__circuito__seccion=seccion).order_by('num_mesa')

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
    

class ResultadosCandidatosView(View):
    template_name = 'resultados_candidatos.html'

    def get(self, request, computo_id):
        computo = Computo.objects.get(pk=computo_id)
        cargos = Cargo.objects.filter(candidatoeleccion__eleccion=computo.eleccion).distinct().order_by('orden_cargo')

        mesas_totales = Mesa.objects.filter(escuela__circuito=computo.eleccion.circuito).count()
        mesas_escrutadas = Mesa.objects.filter(detallecomputo__computo=computo, detallecomputo__cantidad_voto__isnull=False).distinct().count()



        if mesas_totales == 0:
            porcentaje_mesas_escrutadas = 0
        else:
            porcentaje_mesas_escrutadas = (mesas_escrutadas / mesas_totales) * 100

            porcentaje_mesas_escrutadas = round(porcentaje_mesas_escrutadas, 2)

        resultados_cargos = []

        for cargo in cargos:
            candidatos = CandidatoEleccion.objects.filter(
                eleccion=computo.eleccion,
                cargo=cargo
            )

            total_votos_cargo = DetalleComputo.objects.filter(
                computo=computo,
                candidato_eleccion__in=candidatos
            ).aggregate(total=Sum('cantidad_voto'))['total']

            if total_votos_cargo is None:
                total_votos_cargo = 0

            resultados_cargo = []

            for candidato in candidatos:
                cantidad_voto_por_mesa = DetalleComputo.objects.filter(
                    computo=computo,
                    candidato_eleccion=candidato
                ).aggregate(total=Sum('cantidad_voto'))['total']

                cantidad_voto = cantidad_voto_por_mesa if cantidad_voto_por_mesa is not None else 0

                porcentaje = 0
                if total_votos_cargo > 0:
                    porcentaje = (cantidad_voto / total_votos_cargo) * 100

                porcentaje = round(porcentaje, 2)

                resultados_cargo.append({
                    'candidato': candidato,
                    'cantidad_voto': cantidad_voto,
                    'porcentaje': porcentaje
                })

            resultados_cargo.sort(key=lambda x: x['cantidad_voto'], reverse=True)

            resultados_cargos.append({
                'cargo': cargo,
                'resultados': resultados_cargo,
                'total_votos': total_votos_cargo,
            })

        return render(request, self.template_name, {
            'resultados_cargos': resultados_cargos,
            'computo': computo,
            'mesas_totales': mesas_totales,
            'mesas_escrutadas': mesas_escrutadas,
            'porcentaje_mesas_escrutadas': porcentaje_mesas_escrutadas
        })



class ExportarPDFResultadosCandidatosView(View):
    def get(self, request, computo_id):
        computo = Computo.objects.get(pk=computo_id)
        cargos = Cargo.objects.filter(candidatoeleccion__eleccion=computo.eleccion).distinct().order_by('orden_cargo')

        mesas_totales = Mesa.objects.filter(escuela__circuito=computo.eleccion.circuito).count()
        mesas_escrutadas = Mesa.objects.filter(detallecomputo__computo=computo, detallecomputo__cantidad_voto__isnull=False).distinct().count()

        if mesas_totales == 0:
            porcentaje_mesas_escrutadas = 0
        else:
            porcentaje_mesas_escrutadas = (mesas_escrutadas / mesas_totales) * 100

            porcentaje_mesas_escrutadas = round(porcentaje_mesas_escrutadas, 2)

        resultados_cargos = []

        for cargo in cargos:
            candidatos = CandidatoEleccion.objects.filter(
                eleccion=computo.eleccion,
                cargo=cargo
            )

            total_votos_cargo = DetalleComputo.objects.filter(
                computo=computo,
                candidato_eleccion__in=candidatos
            ).aggregate(total=Sum('cantidad_voto'))['total']

            if total_votos_cargo is None:
                total_votos_cargo = 0

            resultados_cargo = []

            for candidato in candidatos:
                cantidad_voto_por_mesa = DetalleComputo.objects.filter(
                    computo=computo,
                    candidato_eleccion=candidato
                ).aggregate(total=Sum('cantidad_voto'))['total']

                cantidad_voto = cantidad_voto_por_mesa if cantidad_voto_por_mesa is not None else 0

                porcentaje = 0
                if total_votos_cargo > 0:
                    porcentaje = (cantidad_voto / total_votos_cargo) * 100

                    porcentaje = round(porcentaje, 2)

                resultados_cargo.append({
                    'candidato': candidato,
                    'cantidad_voto': cantidad_voto,
                    'porcentaje': porcentaje
                })

            resultados_cargo.sort(key=lambda x: x['cantidad_voto'], reverse=True)

            resultados_cargos.append({
                'cargo': cargo,
                'resultados': resultados_cargo,
                'total_votos': total_votos_cargo,
            })

        # Renderiza la plantilla HTML con los datos obtenidos
        template = get_template('exportar_pdf_resultados_candidatos.html')
        html_content = template.render({
            'resultados_cargos': resultados_cargos,
            'computo': computo,
            'mesas_totales': mesas_totales,
            'mesas_escrutadas': mesas_escrutadas,
            'porcentaje_mesas_escrutadas': porcentaje_mesas_escrutadas
        })

        # Crea un objeto HTML a partir del contenido HTML renderizado
        html = HTML(string=html_content)

        # Genera el PDF
        pdf_file = html.write_pdf()

        # Crea una respuesta HTTP con el PDF generado y ábrelo en línea en lugar de descargarlo
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="resultados.pdf"'

        return response