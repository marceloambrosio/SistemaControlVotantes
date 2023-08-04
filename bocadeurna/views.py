from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import DetalleBocaDeUrna, Candidato
from control.models import Circuito, Persona
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

        # Generar el gráfico con Chart.js
        chart_data = {
            'labels': nombres_candidatos,
            'data': votos,
        }

        # Contexto para la plantilla
        context = {
            'circuito': circuito,
            'total_personas_circuito': total_personas_circuito,
            'cantidad_registros_boca_de_urna': cantidad_registros_boca_de_urna,
            'chart_data': chart_data,
            'colores_candidatos': json.dumps(colores_candidatos)
        }
        return render(request, 'bocadeurna/estado_boca_de_urna.html', context)




