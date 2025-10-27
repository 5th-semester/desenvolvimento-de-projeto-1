# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.primeiro_andar_view, name='primeiro_andar'),
    path('segundo-andar/', views.segundo_andar_view, name='segundo_andar'),
    path('api/summary/', views.api_summary, name='api_summary'),
]