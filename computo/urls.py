from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('<int:computo_id>/', views.ComputoMesaListView.as_view(), name='computo_mesa_list'),
    path('<int:computo_id>/<int:mesa_id>/', views.CandidatoEleccionListView.as_view(), name='candidato_eleccion_list'),
]