from django.shortcuts import render, get_object_or_404, redirect
from .forms import VotoForm, NumeroMesaForm
from .models import Persona, Mesa, Circuito, Eleccion
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.generic import ListView
from datetime import datetime, date
from django.db.models import Count,Q
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.contrib.staticfiles import finders
from openpyxl import Workbook
from openpyxl.styles import Alignment
from django.contrib.auth.views import LoginView
import weasyprint
import datetime




# Create your views here.

@login_required(login_url='login')  # Reemplaza 'login' con la URL correspondiente a tu vista de inicio de sesión
def index(request):
    if user_in_group(request.user):
        return redirect('solicitar_numero_mesa')
    if user_in_group_boca_de_urna(request.user):
        return redirect('carga_bocadeurna')
    else:
        circuitos = request.user.circuitos.all()
        context = {'circuitos': circuitos}
        return render(request, 'index_control.html', context)

class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('index'))
        else:
            return super().dispatch(request, *args, **kwargs)

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
    

class PadronListView(View):
    def get(self, request, circuito_id, mesa_id):
        circuito = Circuito.objects.get(pk=circuito_id)
        
        # Obtén el num_mesa de la mesa utilizando el mesa_id
        mesa = Mesa.objects.get(pk=mesa_id)
        num_mesa = mesa.num_mesa

        # Filtra las personas que tienen el mismo mesa_id en su atributo mesa
        personas = Persona.objects.filter(mesa=mesa).order_by('num_orden')

        context = {
            'persona_list': personas,
            'circuito_id': circuito_id,
            'num_mesa': num_mesa,
            'localidad': circuito.localidad
        }

        if 'exportar_pdf' in request.path:
            # Renderiza el contenido de la tabla a HTML utilizando el template
            html_string = render_to_string('padron/padron_list_pdf.html', context)

            # Crea un objeto WeasyPrint a partir del HTML
            pdf = HTML(string=html_string).write_pdf()

            # Devuelve el PDF como respuesta
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="{} - Mesa {}.pdf"'.format(circuito.localidad, num_mesa)
            response.write(pdf)

            return response
        else:
            return render(request, 'padron/padron_list.html', context)
    
def user_in_group(user):
    return user.groups.filter(name='Fiscales').exists()

def user_in_group_boca_de_urna(user):
    return user.groups.filter(name='BocaDeUrna').exists()

@user_passes_test(user_in_group, login_url='login')
def cambiar_voto(request, mesa_id):
    mesa = get_object_or_404(Mesa, pk=mesa_id)

    # Verificar si el usuario tiene acceso al circuito correspondiente a la mesa
    if mesa.escuela.circuito in request.user.circuitos.all():
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
    else:
        # Si el usuario no tiene acceso al circuito correspondiente a la mesa, redirigir a la página de error
        return render(request, 'mesa/mesa_no_existe.html')

@user_passes_test(user_in_group, login_url='login')
def voto_no_existe(request):
    return render(request, 'voto/voto_no_existe.html')

@user_passes_test(user_in_group, login_url='login')
def solicitar_numero_mesa(request):
    if request.method == 'POST':
        form = NumeroMesaForm(request.POST)
        if form.is_valid():
            numero_mesa = form.cleaned_data['numero_mesa']
            mesa = Mesa.objects.filter(num_mesa=numero_mesa).first()
            if mesa:
                return redirect('cambiar_voto', mesa_id=mesa.id) 
            else:
                return redirect('mesa_no_existe')
    else:
        form = NumeroMesaForm()
    
    context = {
        'form': form
    }
    return render(request, 'mesa/solicitar_numero_mesa.html', context)

@user_passes_test(user_in_group, login_url='login')
def mesa_no_existe(request):
    return render(request, 'mesa/mesa_no_existe.html')

class CircuitoDetailView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, circuito_id):
        circuito = get_object_or_404(Circuito, pk=circuito_id)
        if circuito in request.user.circuitos.all():
            # El usuario tiene acceso al circuito, continúa con la lógica de la vista
            mesas = Mesa.objects.filter(escuela__circuito=circuito).annotate(votos_count=Count('persona', filter=Q(persona__voto=True))).order_by('num_mesa')

            for mesa in mesas:
                persona_count = mesa.persona_set.count()
                if persona_count > 0:
                    mesa.porcentaje_votos = round(mesa.votos_count / persona_count * 100, 2)
                else:
                    mesa.porcentaje_votos = 0.0

            form = NumeroMesaForm()
            context = {
                'circuito': circuito,
                'circuito_id': circuito_id,  # Agrega circuito_id al contexto
                'mesas': mesas,
                'form': form,
                'porcentaje_votos_circuito': calcular_porcentaje_votos_circuito(circuito)  # Agrega el porcentaje de votos del circuito al contexto
            }
            return render(request, 'circuito/circuito_detail.html', context)
        else:
            # El usuario no tiene acceso al circuito, redirige a una página de error o realiza otra acción apropiada
            return render(request, 'circuito/circuito_access_denied.html')


    def post(self, request, circuito_id):
        # Obtener el número de mesa de la solicitud POST
        form = NumeroMesaForm(request.POST)

        if form.is_valid():
            num_mesa = form.cleaned_data['num_mesa']
            # Generar la URL inversa con los valores correctos
            url = reverse('padron_list', args=[circuito_id, num_mesa])
            # Redirigir a la URL generada
            return redirect(url)
        else:
            # Manejar caso cuando no se proporciona el número de mesa
            return redirect('mesa_no_existe')
    
def circuito_access_denied(request):
    return render(request, 'circuito/circuito_access_denied.html')

def calcular_porcentaje_votos_circuito(circuito):
    total_personas = Persona.objects.filter(mesa__escuela__circuito=circuito).count()
    total_votos = Persona.objects.filter(mesa__escuela__circuito=circuito, voto=True).count()

    if total_personas > 0:
        porcentaje_votos = (total_votos / total_personas) * 100
        return round(porcentaje_votos, 2)
    else:
        return 0

class CircuitosHabilitadosView(View):
    def get(self, request):
        circuitos = request.user.circuitos.all()
        elecciones = Eleccion.objects.filter(circuito__in=circuitos)

        context = {'circuitos': circuitos, 'elecciones': elecciones}
        return render(request, 'circuito/circuito_habilitado.html', context)


class DetalleMesaView(View):
    def get(self, request, mesa_id):
        mesa = Mesa.objects.get(pk=mesa_id)
        personas = Persona.objects.filter(mesa=mesa).order_by('num_orden')
        
        context = {
            'mesa': mesa,
            'personas': personas
        }
        
        return render(request, 'mesa/detalle_mesa.html', context)

    
class ExportarPDFPersonasSinVotoView(View):
    def get(self, request, circuito_id):
        circuito = get_object_or_404(Circuito, pk=circuito_id)
        personas = Persona.objects.filter(mesa__escuela__circuito=circuito).order_by('domicilio')
        total_personas = personas.count()
        votantes = personas.filter(voto=True).count()
        no_votantes = total_personas - votantes
        porcentaje_votantes = round((votantes / total_personas) * 100, 2) if total_personas > 0 else 0
        
        # Calcular la edad de cada persona
        current_year = datetime.datetime.now().year
        for persona in personas:
            persona.edad = current_year - persona.clase

        context = {
            'persona_list': personas,
            'circuito': circuito,
            'cantidad_personas': total_personas,
            'no_votantes': no_votantes,
            'porcentaje_votantes': porcentaje_votantes,
        }

        # Renderiza el contenido de la tabla a HTML utilizando el template
        html_string = render_to_string('padron/exportar_pdf_personas_sin_voto.html', context)

        # Crea un objeto WeasyPrint a partir del HTML
        pdf = HTML(string=html_string).write_pdf()

        # Devuelve el PDF como respuesta
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="{} - Personas que no votaron.pdf"'.format(circuito.localidad)
        response.write(pdf)

        return response
    

class ExportarPDFPersonasSinVotoMesaView(View):
    def get(self, request, circuito_id, num_mesa):
        personas = Persona.objects.filter(mesa__escuela__circuito_id=circuito_id, mesa_id=num_mesa, voto=False).order_by('num_orden')
        circuito = Circuito.objects.get(pk=circuito_id)
        mesa = Mesa.objects.get(pk=num_mesa)

        context = {
            'persona_list': personas,
            'circuito_id': circuito_id,
            'num_mesa': num_mesa,
            'localidad': circuito.localidad
        }

        # Renderiza el contenido de la tabla a HTML utilizando el template
        html_string = render_to_string('padron/padron_list_pdf.html', context)

        # Crea un objeto WeasyPrint a partir del HTML
        pdf = HTML(string=html_string).write_pdf()

        # Devuelve el PDF como respuesta
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="{} - Mesa {} - Personas que no votaron.pdf"'.format(circuito.localidad, mesa.num_mesa)
        response.write(pdf)

        return response


class ExportarExcelPersonasSinVotoView(View):
    def get(self, request, circuito_id):
        circuito = get_object_or_404(Circuito, pk=circuito_id)
        personas = Persona.objects.filter(mesa__escuela__circuito=circuito)

        # Crear el libro de Excel y la hoja de cálculo
        workbook = Workbook()
        worksheet = workbook.active

        # Agregar los encabezados de las columnas
        worksheet.append(['Apellido y nombre', 'Clase', 'Dirección', 'Escuela - Número de Mesa', 'Voto'])

        # Agregar los datos de las personas a la hoja de cálculo
        for persona in personas:
            voto = "Sí" if persona.voto else "No"
            escuela_mesa = f"{persona.mesa.escuela.nombre}, Mesa: {persona.mesa.num_mesa}"
            worksheet.append([persona.apellido + ', ' + persona.nombre, persona.clase, persona.domicilio, escuela_mesa, voto])

        # Ajustar el ancho de las columnas
        worksheet.column_dimensions['A'].width = 30
        worksheet.column_dimensions['B'].width = 10
        worksheet.column_dimensions['C'].width = 30
        worksheet.column_dimensions['D'].width = 25
        worksheet.column_dimensions['E'].width = 10

        # Configurar la respuesta para descargar el archivo
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{circuito.localidad}_personas_voto.xlsx"'

        # Guardar el libro de Excel en la respuesta
        workbook.save(response)

        return response