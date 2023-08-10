from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index_reportes, name="index_reportes"),
    path('estado_mesas/<int:circuito_id>/', login_required(views.EstadoMesasView.as_view()), name='estado_mesas'),
    path('circuitos_habilitados/', login_required(views.CircuitosHabilitadosView.as_view()), name='circuitos_habilitados_reportes'),
    path('estado_mesas_boca_de_urna/<int:circuito_id>/', views.EstadoMesasBocaDeUrnaView.as_view(), name='estado_mesas_boca_de_urna')
]