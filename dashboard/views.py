# 5th-semester/desenvolvimento-de-projeto-1/desenvolvimento-de-projeto-1-interface-projeto/dashboard/views.py

from django.shortcuts import render
from .dados_estaticos import dados_primeiro_andar, dados_segundo_andar
from django.http import HttpResponse

def primeiro_andar_view(request):
    """
    View para a página do primeiro andar.
    
    Busca os dados estáticos do primeiro andar e os envia para o template.
    O contexto 'dados_primeiro_andar' conterá a lista de medições.
    """
    context = {
        'titulo': 'Primeiro Andar',
        'dados_primeiro_andar': dados_primeiro_andar,
    }
    return render(request, 'dashboard/primeiro_andar.html', context)

def segundo_andar_view(request):
    """
    View para a página do segundo andar.
    
    Busca os dados estáticos do segundo andar e os envia para o template.
    O contexto 'dados_segundo_andar' conterá a lista de medições.
    """
    context = {
        'titulo': 'Segundo Andar',
        'dados_segundo_andar': dados_segundo_andar,
    }
    return render(request, 'dashboard/segundo_andar.html', context)
