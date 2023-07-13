from django.urls import path
from . import views
from .views import cambiar_voto, solicitar_numero_mesa, mesa_no_existe

urlpatterns = [
    path('', views.index, name="index_control"),
    path('padron_list/', views.PadronListView.as_view(), name="padron_list"),
    path('solicitar_numero_mesa/', solicitar_numero_mesa, name='solicitar_numero_mesa'),
    path('mesa/<int:mesa_id>/cambiar-voto/', cambiar_voto, name='cambiar_voto'),
    path('mesa_no_existe/', mesa_no_existe, name='mesa_no_existe'),
]