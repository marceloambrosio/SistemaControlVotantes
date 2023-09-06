from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('<int:computo_id>/', views.ComputoMesaListView.as_view(), name='computo_mesa_list'),
    path('<int:computo_id>/<int:mesa_id>/', views.DetalleComputoMesaView.as_view(), name='detalle_computo_mesa'),
]