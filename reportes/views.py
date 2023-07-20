from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from control.models import Mesa, Circuito

# Create your views here.

@login_required(login_url='login')  # Reemplaza 'login' con la URL correspondiente a tu vista de inicio de sesión
def index(request):
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