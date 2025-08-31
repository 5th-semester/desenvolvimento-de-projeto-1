# dashboard/urls.py


from django.urls import path
from . import views

urlpatterns = [
    # Quando o endereço for 'dashboard/', chame a função 'index' de views.py
    path('', views.index, name='dashboard_home'),
]

'''
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rede.urls')),  # Adicione esta linha
]'''