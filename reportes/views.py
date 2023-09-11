from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from control.models import Mesa, Circuito, Mesa, Persona, Eleccion
from bocadeurna.models import BocaDeUrna, DetalleBocaDeUrna, CandidatoEleccion
from computo.models import Computo
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
    def get(self, request, circuito_id, eleccion_id):
        # Obtener el circuito correspondiente al circuito_id
        circuito = get_object_or_404(Circuito, pk=circuito_id)
        
        # Obtener las mesas asociadas al circuito
        mesas = Mesa.objects.filter(escuela__circuito=circuito)

        # Calcular el porcentaje de votos para cada mesa
        for mesa in mesas:
            persona_count = mesa.persona_set.count()
            if persona_count > 0:
                votos_count = mesa.persona_set.filter(voto=True).count()
                mesa.porcentaje_votos = round(votos_count / persona_count * 100, 2)
            else:
                mesa.porcentaje_votos = 0.0

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

        # Calcular el total de personas en el circuito
        total_personas_circuito = Persona.objects.filter(mesa__escuela__circuito=circuito).count()

        # Obtener la lista de candidatos para este circuito y elección
        candidatos = CandidatoEleccion.objects.filter(eleccion_id=eleccion_id)


        # Realizar los cálculos y operaciones necesarias para los datos de boca de urna
        candidatos_ordenados = []
        porcentaje = 0.0  # Valor por defecto en caso de que no haya registros de boca de urna
        candidatos_ordenados_con_porcentaje = []

        if total_personas_circuito > 0:
            chart_labels = [candidato.candidato.nombre + " " + candidato.candidato.apellido for candidato in candidatos]
            chart_data = [detalles_boca_de_urna.filter(candidato=candidato).count() for candidato in candidatos]
            colores_candidatos = {candidato.candidato.nombre + " " + candidato.candidato.apellido: candidato.candidato.color for candidato in candidatos}
            
            candidatos_ordenados = sorted(zip(chart_labels, chart_data), key=lambda x: x[1], reverse=True)
            candidatos_ordenados_con_porcentaje = []

            if cantidad_registros_boca_de_urna > 0:
                candidatos_ordenados_con_porcentaje = [(nombre, votos, (votos / cantidad_registros_boca_de_urna) * 100) for nombre, votos in candidatos_ordenados]
            else:
                candidatos_ordenados_con_porcentaje = [(candidato.candidato.nombre + " " + candidato.candidato.apellido, 0, 0.0) for candidato in candidatos]

            
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
            'tipo_eleccion': tipo_eleccion,
        }

        return render(request, 'info/estado_mesa_y_boca_de_urna.html', context)

    
class CircuitosHabilitadosView(View):
    def get(self, request):
        # Obtén los circuitos habilitados del usuario
        circuitos_habilitados = request.user.circuitos.all()
        
        # Inicializa una lista para almacenar las elecciones con sus computo_ids
        elecciones_con_computo = []
        
        # Recorre los circuitos habilitados para obtener las elecciones con computo_ids
        for circuito in circuitos_habilitados:
            # Obtén las elecciones relacionadas con el circuito
            elecciones = circuito.eleccion_set.all()
            
            # Para cada elección, obtén el computo_id si existe y agrega la elección con el computo_id a la lista
            for eleccion in elecciones:
                computo = Computo.objects.filter(eleccion=eleccion).first()
                if computo:
                    eleccion.computo_id = computo.id
                    elecciones_con_computo.append(eleccion)
        
        # Imprime las elecciones con computo_ids en la consola para depurar
        for eleccion in elecciones_con_computo:
            print(f"Eleccion: {eleccion.id}, Computo ID: {eleccion.computo_id}")
        
        context = {'elecciones': elecciones_con_computo}
        return render(request, 'circuitos/circuito_habilitado.html', context)

