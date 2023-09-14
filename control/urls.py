from django.urls import path
from . import views
from .views import cambiar_voto, voto_no_existe, solicitar_numero_mesa, mesa_no_existe, circuito_access_denied
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name="index"),
    #path('', views.index, name='index'),
    path('solicitar_numero_mesa/', login_required(solicitar_numero_mesa), name='solicitar_numero_mesa'),
    path('mesa_no_existe/', login_required(mesa_no_existe), name='mesa_no_existe'),
    path('mesa/<int:mesa_id>/cambiar-voto/', login_required(cambiar_voto), name='cambiar_voto'),
    path('mesa/<int:mesa_id>/detalle/', login_required(views.DetalleMesaView.as_view()), name='detalle_mesa'),
    path('voto_no_existe/', login_required(voto_no_existe), name='voto_no_existe'),
    path('padron_list/<int:circuito_id>/<int:mesa_id>/', login_required(views.PadronListView.as_view()), name="padron_list"),
    path('circuito/<int:circuito_id>/', login_required(views.CircuitoDetailView.as_view()), name='circuito_detail'),
    path('circuito_access_denied/', login_required(circuito_access_denied), name='circuito_access_denied'),
    path('circuitos_habilitados/', login_required(views.CircuitosHabilitadosView.as_view()), name='circuitos_habilitados'),
    path('exportar_pdf/<int:circuito_id>/<int:mesa_id>/', login_required(views.PadronListView.as_view()), name='exportar_pdf'),
    path('exportar_pdf_personas_sin_voto_mesa/<int:circuito_id>/<int:mesa_id>/', views.ExportarPDFPersonasSinVotoMesaView.as_view(), name='exportar_pdf_personas_sin_voto_mesa'),
    path('exportar_pdf_personas_sin_voto/<int:circuito_id>/', login_required(views.ExportarPDFPersonasSinVotoView.as_view()), name='exportar_pdf_personas_sin_voto'),
    path('exportar_excel_personas_sin_voto/<int:circuito_id>/', login_required(views.ExportarExcelPersonasSinVotoView.as_view()), name='exportar_excel_personas_sin_voto'),
]