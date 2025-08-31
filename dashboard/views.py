# dashboard/views.py

from django.shortcuts import render
from .dados_estaticos import dados_primeiro_andar, dados_segundo_andar
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Bem-vindo ao Dashboard!</h1>")

def primeiro_andar(request):
    """
    View para a página do primeiro andar.
    
    Busca os dados estáticos do primeiro andar e os envia para o template.
    O contexto 'dados' conterá a lista de medições.
    """
    context = {
        'titulo': 'Primeiro Andar',
        'dados': dados_primeiro_andar,
    }
    return render(request, 'primeiro_andar.html', context)

def segundo_andar(request):
    """
    View para a página do segundo andar.
    
    Busca os dados estáticos do segundo andar e os envia para o template.
    O contexto 'dados' conterá a lista de medições.
    """
    context = {
        'titulo': 'Segundo Andar',
        'dados': dados_segundo_andar,
    }
    return render(request, 'segundo_andar.html', context)