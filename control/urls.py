from django.urls import path
from . import views
from .views import cambiar_voto, voto_no_existe, solicitar_numero_mesa, mesa_no_existe

urlpatterns = [
    path('', views.index, name="index_control"),
    path('padron_list/', views.PadronListView.as_view(), name="padron_list"),
    path('solicitar_numero_mesa/', solicitar_numero_mesa, name='solicitar_numero_mesa'),
    path('voto_no_existe/', voto_no_existe, name='voto_no_existe'),
    path('mesa/<int:mesa_id>/cambiar-voto/', cambiar_voto, name='cambiar_voto'),
    path('mesa_no_existe/', mesa_no_existe, name='mesa_no_existe'),
    path('circuito/<int:circuito_id>/', views.CircuitoDetailView.as_view(), name='circuito_detail'),
]