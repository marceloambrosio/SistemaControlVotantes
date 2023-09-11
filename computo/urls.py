from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('<int:computo_id>/', login_required(views.ComputoMesaListView.as_view()), name='computo_mesa_list'),
    path('<int:computo_id>/<int:mesa_id>/<int:cargo_id>', login_required(views.DetalleComputoMesaView.as_view()), name='detalle_computo_mesa'),
    path('resultados/<int:computo_id>/', login_required(views.ResultadosCandidatosView.as_view()), name='resultados_candidatos'),
    path('pdf_resultados/<int:computo_id>/', login_required(views.ExportarPDFResultadosCandidatosView.as_view()), name='pdf_resultados_candidatos'),
    path('circuitos_habilitados/', login_required(views.CircuitosHabilitadosView.as_view()), name='circuitos_habilitados_computo'),
]