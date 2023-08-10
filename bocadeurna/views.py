from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import DetalleBocaDeUrna, Candidato, BocaDeUrna
from control.models import Circuito, Persona
from .forms import DetalleBocaDeUrnaForm
import json

# Create your views here.

@login_required(login_url='login')  # Reemplaza 'login' con la URL correspondiente a tu vista de inicio de sesión
def index_bocadeurna(request):
    return render(request, 'index_bocadeurna.html')


class EstadoBocaDeUrnaView(View):
    def get(self, request, circuito_id):
        # Obtener el circuito correspondiente al circuito_id
        circuito = get_object_or_404(Circuito, pk=circuito_id)

        # Obtener los detalles de boca de urna asociados al circuito
        detalles_boca_de_urna = DetalleBocaDeUrna.objects.filter(boca_de_urna__circuito=circuito)

        # Calcular el total de personas que tiene el circuito
        total_personas_circuito = Persona.objects.filter(mesa__escuela__circuito=circuito).count()

        # Calcular la cantidad de registros de boca de urna del circuito
        cantidad_registros_boca_de_urna = detalles_boca_de_urna.count()

        # Obtener los datos necesarios para el gráfico
        candidatos = Candidato.objects.filter(circuito=circuito)
        nombres_candidatos = [candidato.nombre + " " + candidato.apellido for candidato in candidatos]
        votos = [detalles_boca_de_urna.filter(candidato=candidato).count() for candidato in candidatos]
        colores_candidatos = {candidato.nombre + " " + candidato.apellido: candidato.color for candidato in candidatos}

        # Ordenar los candidatos por votos de mayor a menor
        candidatos_ordenados = sorted(zip(nombres_candidatos, votos), key=lambda x: x[1], reverse=True)

        # Calcular los votos totales de los candidatos restantes (no incluidos en el top 3)
        otros_votos = sum(votos for _, votos in candidatos_ordenados[3:])

        # Calcular los porcentajes de votos para cada candidato
        if cantidad_registros_boca_de_urna > 0:
            candidatos_ordenados_con_porcentaje = [(nombre, votos, (votos / cantidad_registros_boca_de_urna) * 100) for nombre, votos in candidatos_ordenados]
        else:
            candidatos_ordenados_con_porcentaje = [(candidato.nombre + " " + candidato.apellido, 0, 0.0) for candidato in candidatos]

        # Crear los datos para el gráfico
        chart_labels = [nombre for nombre, _, _ in candidatos_ordenados_con_porcentaje[:3]] + ["Otros"]
        chart_data = [votos for _, votos, _ in candidatos_ordenados_con_porcentaje[:3]] + [otros_votos]

        # Calcular el porcentaje de registros de Boca de Urna con respecto a personas en el circuito
        if cantidad_registros_boca_de_urna > 0:
            porcentaje = (cantidad_registros_boca_de_urna / total_personas_circuito) * 100
        else:
            porcentaje = 0

        # Contexto para la plantilla
        context = {
            'circuito': circuito,
            'total_personas_circuito': total_personas_circuito,
            'cantidad_registros_boca_de_urna': cantidad_registros_boca_de_urna,
            'chart_labels': json.dumps(chart_labels),
            'chart_data': json.dumps(chart_data),
            'colores_candidatos': json.dumps(colores_candidatos),
            'porcentaje': porcentaje,
            'candidatos_ordenados': candidatos_ordenados_con_porcentaje,
        }
        return render(request, 'bocadeurna/estado_boca_de_urna.html', context)



@login_required
def carga_boca_de_urna(request):
    circuito_usuario = request.user.circuitos.first()

    if not circuito_usuario:
        return render(request, 'error.html', {'error_message': 'No tiene circuitos habilitados.'})

    bocas_de_urna = BocaDeUrna.objects.filter(circuito=circuito_usuario)

    if request.method == 'POST':
        form = DetalleBocaDeUrnaForm(request.POST, circuito_usuario=circuito_usuario)
        if form.is_valid():
            detalle_boca_de_urna = form.save(commit=False)
            if bocas_de_urna.exists():
                # Asignar la boca de urna correspondiente al detalle
                detalle_boca_de_urna.boca_de_urna = bocas_de_urna.first()
                # Asignar el circuito del candidato seleccionado
                candidato_seleccionado = form.cleaned_data['candidato']
                detalle_boca_de_urna.circuito = candidato_seleccionado.circuito
                detalle_boca_de_urna.save()
            else:
                # Manejar el caso en el que no haya boletas de boca de urna asociadas al circuito del usuario
                return render(request, 'error.html', {'error_message': 'No hay boletas de boca de urna asociadas a su circuito.'})
            return redirect('carga_success_bocadeurna')
    else:
        form = DetalleBocaDeUrnaForm(circuito_usuario=circuito_usuario)  # Pasamos el circuito_usuario al formulario
        # Excluir la opción en blanco de los candidatos
        form.fields['candidato'].queryset = Candidato.objects.filter(circuito=circuito_usuario).exclude(nombre__isnull=True)

    context = {
        'bocas_de_urna': zip(bocas_de_urna, [DetalleBocaDeUrna.objects.filter(boca_de_urna=boca_de_urna) for boca_de_urna in bocas_de_urna]),
        'form': form,
        'circuito': circuito_usuario.localidad,
    }

    return render(request, 'bocadeurna/carga_boca_de_urna.html', context)


@login_required
def carga_sucess_boca_de_urna(request):
    return render(request, 'bocadeurna/success_boca_de_urna.html')
    