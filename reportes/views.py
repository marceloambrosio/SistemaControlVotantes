from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from control.models import Mesa, Circuito
from control.models import Circuito, Mesa, Persona
from bocadeurna.models import DetalleBocaDeUrna, Candidato
import json

# Create your views here.

@login_required(login_url='login')  # Reemplaza 'login' con la URL correspondiente a tu vista de inicio de sesión
def index_reportes(request):
    return render(request, 'index_reportes.html')


class EstadoMesasView(View):
    def get(self, request, circuito_id):
        circuito = Circuito.objects.get(pk=circuito_id)
        mesas = Mesa.objects.filter(escuela__circuito=circuito)

        for mesa in mesas:
            persona_count = mesa.persona_set.count()
            if persona_count > 0:
                votos_count = mesa.persona_set.filter(voto=True).count()
                mesa.porcentaje_votos = round(votos_count / persona_count * 100, 2)
            else:
                mesa.porcentaje_votos = 0.0

        context = {
            'circuito': circuito,
            'mesas': mesas
        }

        return render(request, 'mesas/estado_mesas.html', context)
    
class EstadoMesasBocaDeUrnaView(View):
    def get(self, request, circuito_id):
        circuito = Circuito.objects.get(pk=circuito_id)
        
        # Obtener los datos para el estado de mesas (similar a tu EstadoMesasView)
        mesas = Mesa.objects.filter(escuela__circuito=circuito)
        for mesa in mesas:
            persona_count = mesa.persona_set.count()
            if persona_count > 0:
                votos_count = mesa.persona_set.filter(voto=True).count()
                mesa.porcentaje_votos = round(votos_count / persona_count * 100, 2)
            else:
                mesa.porcentaje_votos = 0.0
        
        # Obtener los datos para el estado de boca de urna (similar a tu EstadoBocaDeUrnaView)
        detalles_boca_de_urna = DetalleBocaDeUrna.objects.filter(boca_de_urna__circuito=circuito)
        total_personas_circuito = Persona.objects.filter(mesa__escuela__circuito=circuito).count()
        cantidad_registros_boca_de_urna = detalles_boca_de_urna.count()
        candidatos = Candidato.objects.filter(circuito=circuito)
        
        # Realizar los cálculos y operaciones necesarias para los datos de boca de urna
        candidatos_ordenados = []
        porcentaje = 0.0  # Valor por defecto en caso de que no haya registros de boca de urna

        if total_personas_circuito > 0:
            chart_labels = [candidato.nombre + " " + candidato.apellido for candidato in candidatos]
            chart_data = [detalles_boca_de_urna.filter(candidato=candidato).count() for candidato in candidatos]
            colores_candidatos = {candidato.nombre + " " + candidato.apellido: candidato.color for candidato in candidatos}
            
            candidatos_ordenados = sorted(zip(chart_labels, chart_data), key=lambda x: x[1], reverse=True)
            candidatos_ordenados_con_porcentaje = []

            if cantidad_registros_boca_de_urna > 0:
                candidatos_ordenados_con_porcentaje = [(nombre, votos, (votos / cantidad_registros_boca_de_urna) * 100) for nombre, votos in candidatos_ordenados]
            else:
                candidatos_ordenados_con_porcentaje = [(candidato.nombre + " " + candidato.apellido, 0, 0.0) for candidato in candidatos]

            
            if cantidad_registros_boca_de_urna > 0:
                porcentaje = (cantidad_registros_boca_de_urna / total_personas_circuito) * 100
            else:
                porcentaje == 0
                    
        context = {
            'circuito': circuito,
            'mesas': mesas,
            'total_personas_circuito': total_personas_circuito,
            'cantidad_registros_boca_de_urna': cantidad_registros_boca_de_urna,
            'chart_labels': json.dumps(chart_labels) if total_personas_circuito > 0 else json.dumps([]),
            'chart_data': json.dumps(chart_data) if total_personas_circuito > 0 else json.dumps([]),
            'colores_candidatos': json.dumps(colores_candidatos) if total_personas_circuito > 0 else json.dumps({}),
            'porcentaje': porcentaje,
            'candidatos_ordenados': candidatos_ordenados_con_porcentaje,
        }

        return render(request, 'info/estado_mesa_y_boca_de_urna.html', context)

    
class CircuitosHabilitadosView(View):
    def get(self, request):
        circuitos = request.user.circuitos.all()

        context = {'circuitos': circuitos}
        return render(request, 'circuitos/circuito_habilitado.html', context)