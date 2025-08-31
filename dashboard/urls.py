# dashboard/urls.py

from django.urls import path
from .templates.dashboard import views

urlpatterns = [
    # Quando o endereço for 'dashboard/', chame a função 'index' de views.py
    path('', views.index, name='dashboard_home'),
]