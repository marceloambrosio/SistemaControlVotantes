from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index_bocadeurna, name="index_bocadeurna"),
    path('estado/<int:circuito_id>/', login_required(views.EstadoBocaDeUrnaView.as_view()), name='bocadeurna'),
]