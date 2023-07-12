from django.urls import path
from . import views
from .views import cambiar_voto

urlpatterns = [
    path('', views.index, name="index_control"),
    path('padron_list/', views.PadronListView.as_view(), name="padron_list"),
    path('mesa/<int:mesa_id>/cambiar-voto/', cambiar_voto, name='cambiar_voto'),
]