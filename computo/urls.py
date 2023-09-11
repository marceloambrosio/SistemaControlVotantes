from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('<int:computo_id>/', views.ComputoMesaListView.as_view(), name='computo_mesa_list'),
    path('<int:computo_id>/<int:mesa_id>/<int:cargo_id>', views.DetalleComputoMesaView.as_view(), name='detalle_computo_mesa'),
    path('resultados/<int:computo_id>/', views.ResultadosCandidatosView.as_view(), name='resultados_candidatos'),
    path('pdf_resultados/<int:computo_id>/', views.ExportarPDFResultadosCandidatosView.as_view(), name='pdf_resultados_candidatos'),
]