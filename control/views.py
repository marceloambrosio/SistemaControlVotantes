from django.shortcuts import render, get_object_or_404, redirect
from .forms import VotoForm
from .models import Persona, Mesa
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.generic import ListView
from datetime import datetime

# Create your views here.

def index(request):
    return render(request, 'index_control.html')

class PadronDatatableView(BaseDatatableView):
    model = Persona
    columns = ('apellido', 'nombre', 'dni', 'clase', 'mesa.num_mesa','mesa.escuela.nombre','voto')
    order_columns = ['apellido', 'nombre','clase']

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

def cambiar_voto(request, mesa_id):
    mesa = get_object_or_404(Mesa, pk=mesa_id)

    if request.method == 'POST':
        form = VotoForm(request.POST)
        if form.is_valid():
            num_orden = form.cleaned_data['num_orden']
            persona = get_object_or_404(Persona, num_orden=num_orden, mesa=mesa)
            persona.voto = True
            persona.save()
            return render(request, 'voto/voto_success.html', {'mesa': mesa, 'persona': persona})
    else:
        form = VotoForm()

    return render(request, 'voto/cambiar_voto.html', {'form': form, 'mesa': mesa})