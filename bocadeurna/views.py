from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views import View
from django.db.models import Q
from .models import DetalleBocaDeUrna, BocaDeUrna
from control.models import Circuito, Persona, Eleccion, TipoEleccion
from computo.models import CandidatoEleccion, Candidato
from .forms import DetalleBocaDeUrnaForm
import json

# Create your views here.

@login_required(login_url='login')  # Reemplaza 'login' con la URL correspondiente a tu vista de inicio de sesión
def index_bocadeurna(request):
    return render(request, 'index_bocadeurna.html')


def user_in_group_boca_de_urna(user):
    return user.groups.filter(name='BocaDeUrna').exists()


class EstadoBocaDeUrnaView(View):
    def get(self, request, circuito_id, eleccion_id):
        # Obtener el circuito correspondiente al circuito_id
        circuito = get_object_or_404(Circuito, pk=circuito_id)

        # Obtener todas las elecciones en ese circuito
        elecciones = Eleccion.objects.filter(circuito=circuito)

        # Filtrar la elección correspondiente a eleccion_id, si existe
        eleccion = elecciones.filter(pk=eleccion_id).first()

        bocas_de_urna = BocaDeUrna.objects.filter(eleccion__circuito=circuito)

        # Obtener el objeto TipoEleccion a través de la relación en Eleccion
        tipo_eleccion = eleccion.tipo_eleccion.nombre

         # Filtrar los detalles de boca de urna asociados al circuito y la elección seleccionada
        detalles_boca_de_urna = DetalleBocaDeUrna.objects.filter(
            boca_de_urna__in=bocas_de_urna,
            candidato__in=CandidatoEleccion.objects.filter(eleccion=eleccion),
        )

        # Calcular la cantidad de registros de boca de urna del circuito y la elección seleccionada
        cantidad_registros_boca_de_urna = detalles_boca_de_urna.count()

        # Calcular el total de personas que tiene el circuito
        total_personas_circuito = Persona.objects.filter(mesa__escuela__circuito=circuito).count()

        # Calcular la cantidad de registros de boca de urna del circuito
        cantidad_registros_boca_de_urna = detalles_boca_de_urna.count()

        # Obtener los datos necesarios para el gráfico
        #candidatos = CandidatoEleccion.get_available_candidates(circuito, tipo_eleccion)  # Obtener los candidatos de esta elección
        candidatos = CandidatoEleccion.objects.filter(eleccion=eleccion)
        
        #candidatos = Candidato.objects.filter(circuito=circuito)
        nombres_candidatos = [candidato.candidato.nombre + " " + candidato.candidato.apellido for candidato in candidatos]
        votos = [detalles_boca_de_urna.filter(candidato=candidato).count() for candidato in candidatos]
        colores_candidatos = {candidato.candidato.nombre + " " + candidato.candidato.apellido: candidato.candidato.color for candidato in candidatos}

        # Ordenar los candidatos por votos de mayor a menor
        candidatos_ordenados = sorted(zip(nombres_candidatos, votos), key=lambda x: x[1], reverse=True)

        # Calcular los votos totales de los candidatos restantes (no incluidos en el top 3)
        otros_votos = sum(votos for _, votos in candidatos_ordenados[3:])

        # Calcular los porcentajes de votos para cada candidato
        if cantidad_registros_boca_de_urna > 0:
            candidatos_ordenados_con_porcentaje = [(nombre, votos, (votos / cantidad_registros_boca_de_urna) * 100) for nombre, votos in candidatos_ordenados]
        else:
            candidatos_ordenados_con_porcentaje = [(candidato.candidato.nombre + " " + candidato.candidato.apellido, 0, 0.0) for candidato in candidatos]

        # Crear los datos para el gráfico
        chart_labels = [nombre for nombre, _, _ in candidatos_ordenados_con_porcentaje[:3]] + ["Otros"]
        chart_data = [votos for _, votos, _ in candidatos_ordenados_con_porcentaje[:3]] + [otros_votos]

        # Calcular el porcentaje de registros de Boca de Urna con respecto a personas en el circuito
        if cantidad_registros_boca_de_urna > 0 and total_personas_circuito > 0:
            porcentaje = (cantidad_registros_boca_de_urna / total_personas_circuito) * 100
        else:
            porcentaje = 0

        # Contexto para la plantilla
        context = {
            'circuito': circuito,
            'eleccion': eleccion,
            'total_personas_circuito': total_personas_circuito,
            'cantidad_registros_boca_de_urna': cantidad_registros_boca_de_urna,
            'chart_labels': json.dumps(chart_labels),
            'chart_data': json.dumps(chart_data),
            'colores_candidatos': json.dumps(colores_candidatos),
            'porcentaje': porcentaje,
            'candidatos_ordenados': candidatos_ordenados_con_porcentaje,
            'tipo_eleccion': tipo_eleccion,
        }
        return render(request, 'bocadeurna/estado_boca_de_urna.html', context)



@user_passes_test(user_in_group_boca_de_urna, login_url='login')
def carga_boca_de_urna(request):
    usuario = request.user
    circuitos_usuario = usuario.circuitos.all()

    if not circuitos_usuario.exists():
        return render(request, 'error.html', {'error_message': 'No tiene circuitos habilitados.'})

    bocas_de_urna = BocaDeUrna.objects.filter(eleccion__circuito__in=circuitos_usuario)

    if request.method == 'POST':
        form = DetalleBocaDeUrnaForm(request.POST)
        if form.is_valid():
            detalle_boca_de_urna = form.save(commit=False)
            detalle_boca_de_urna.boca_de_urna = bocas_de_urna.first()

            candidatos_disponibles = CandidatoEleccion.objects.filter(
                Q(eleccion__circuito__in=circuitos_usuario) & Q(eleccion=usuario.eleccion)
            )
            candidato_seleccionado = form.cleaned_data['candidato']
            
            if candidato_seleccionado in candidatos_disponibles:
                detalle_boca_de_urna.candidato = candidato_seleccionado
                detalle_boca_de_urna.save()
                return redirect('carga_success_bocadeurna')
            else:
                error_message = 'El candidato seleccionado no está disponible para esta elección y circuito.'
                return render(request, 'error.html', {'error_message': error_message})
    else:
        form = DetalleBocaDeUrnaForm()

        candidatos_disponibles = CandidatoEleccion.objects.filter(
            Q(eleccion__circuito__in=circuitos_usuario) & Q(eleccion=usuario.eleccion)
        )
        form.fields['candidato'].queryset = candidatos_disponibles

    context = {
        'bocas_de_urna': zip(bocas_de_urna, [DetalleBocaDeUrna.objects.filter(boca_de_urna=boca_de_urna) for boca_de_urna in bocas_de_urna]),
        'form': form,
        'circuito': usuario.circuitos.first().localidad,  # Aquí tomo el primer circuito del usuario para obtener la localidad
    }

    return render(request, 'bocadeurna/carga_boca_de_urna.html', context)






@user_passes_test(user_in_group_boca_de_urna, login_url='login')
def carga_sucess_boca_de_urna(request):
    return render(request, 'bocadeurna/success_boca_de_urna.html')
    