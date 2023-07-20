from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name="index"),
    path('estado_mesas/<int:circuito_id>/', views.EstadoMesasView.as_view(), name='estado_mesas'),
]