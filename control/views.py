from django.shortcuts import render, get_object_or_404, redirect
from .forms import VotoForm, NumeroMesaForm
from .models import Persona, Mesa, Circuito
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.generic import ListView
from datetime import datetime
from django.db.models import Count,Q
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

def index(request):
    circuitos = request.user.circuitos.all()
    context = {'circuitos': circuitos}
    return render(request, 'index_control.html', context)

class PadronDatatableView(BaseDatatableView):
    model = Persona
    columns = ('apellido', 'nombre', 'dni', 'clase', 'mesa.num_mesa','mesa.escuela.nombre','voto')
    order_columns = ['voto','apellido', 'nombre','clase']

    def get_initial_queryset(self):
        return Persona.objects.all()

    def get_filter_method(self):
        return self.FILTER_ICONTAINS
    
    def filter_queryset(self, qs):
        filter_customer = self.request.POST.get('search[value]', None)

        if filter_customer:
            customer_parts = filter_customer.strip().split(' ')
            qs_params = Q()
            for part in customer_parts:
                qs_params &= Q(apellido__icontains=part) | Q(nombre__icontains=part) | Q(dni__icontains=part)
            qs = qs.filter(qs_params)
        return qs
    

class PadronListView(ListView):
    model = Persona
    template_name = 'padron/padron_list.html'
    ordering = ['apellido', 'nombre','clase']

    def get_queryset(self):
        queryset = super().get_queryset()
        circuitos = self.request.user.circuitos.all()
        return queryset.filter(mesa__escuela__circuito__in=circuitos)
    
    

def cambiar_voto(request, mesa_id):
    mesa = get_object_or_404(Mesa, pk=mesa_id)

    if request.method == 'POST':
        form = VotoForm(request.POST)
        if form.is_valid():
            num_orden = form.cleaned_data['num_orden']
            persona = Persona.objects.filter(num_orden=num_orden, mesa=mesa).first()
            if persona:
                persona.voto = True
                persona.save()
                return render(request, 'voto/voto_success.html', {'mesa': mesa, 'persona': persona})
            else:
                return render(request, 'voto/voto_no_existe.html', {'mesa_id': mesa_id, 'num_orden': num_orden})
    else:
        form = VotoForm()

    return render(request, 'voto/cambiar_voto.html', {'form': form, 'mesa': mesa})

def voto_no_existe(request):
    return render(request, 'voto/voto_no_existe.html')

def solicitar_numero_mesa(request):
    if request.method == 'POST':
        form = NumeroMesaForm(request.POST)
        if form.is_valid():
            numero_mesa = form.cleaned_data['numero_mesa']
            mesa = Mesa.objects.filter(num_mesa=numero_mesa).first()
            if mesa:
                return redirect('cambiar_voto', mesa_id=numero_mesa)
            else:
                return redirect('mesa_no_existe')
    else:
        form = NumeroMesaForm()
    
    context = {
        'form': form
    }
    return render(request, 'mesa/solicitar_numero_mesa.html', context)

def mesa_no_existe(request):
    return render(request, 'mesa/mesa_no_existe.html')

class CircuitoDetailView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, circuito_id):
        circuito = get_object_or_404(Circuito, pk=circuito_id)
        mesas = Mesa.objects.filter(escuela__circuito=circuito).annotate(votos_count=Count('persona', filter=Q(persona__voto=True)))

        for mesa in mesas:
            persona_count = mesa.persona_set.count()
            mesa.porcentaje_votos = round(mesa.votos_count / persona_count * 100, 2)

        context = {
            'circuito': circuito,
            'mesas': mesas
        }
        return render(request, 'circuito/circuito_detail.html', context)
    
    def get(self, request, circuito_id):
        circuito = get_object_or_404(Circuito, pk=circuito_id)
        if circuito in request.user.circuitos.all():
            # El usuario tiene acceso al circuito, continúa con la lógica de la vista
            mesas = Mesa.objects.filter(escuela__circuito=circuito).annotate(votos_count=Count('persona', filter=Q(persona__voto=True)))

            for mesa in mesas:
                persona_count = mesa.persona_set.count()
                mesa.porcentaje_votos = round(mesa.votos_count / persona_count * 100, 2)

            context = {
                'circuito': circuito,
                'mesas': mesas
            }
            return render(request, 'circuito/circuito_detail.html', context)
        else:
            # El usuario no tiene acceso al circuito, redirige a una página de error o realiza otra acción apropiada
            return render(request, 'circuito/circuito_access_denied.html')
    
def circuito_access_denied(request):
    return render(request, 'circuito/circuito_access_denied.html')


class CircuitosHabilitadosView(View):
    @method_decorator(login_required)
    def get(self, request):
        circuitos = request.user.circuitos.all()
        context = {'circuitos': circuitos}
        return render(request, 'circuito/circuito_habilitado.html', context)