# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Documentação: A URL raiz ('') agora chama a view do primeiro andar.
    path('', views.primeiro_andar_view, name='primeiro_andar'),
    # Documentação: Uma nova URL para o segundo andar.
    path('segundo-andar/', views.segundo_andar_view, name='segundo_andar'),
]