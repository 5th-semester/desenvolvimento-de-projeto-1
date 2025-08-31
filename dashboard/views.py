# dashboard/views.py

from django.shortcuts import render
from .dados_estaticos import dados_primeiro_andar, dados_segundo_andar
from django.http import HttpResponse
'''
def index(request):
    """
    Esta view será responsável por renderizar a página principal do dashboard.
    """
    # Documentação: Vamos substituir os dados de exemplo dos cômodos
    # por uma lista que representa exatamente os dados da sua imagem.
    # Cada item do dicionário é uma linha da tabela.
    sinais_mock = [
        {'id': 1, 'dbm': -60, 'download': 540, 'upload': 540, 'interferencia': 0},
        {'id': 2, 'dbm': -68, 'download': 324, 'upload': 396, 'interferencia': 0},
        {'id': 3, 'dbm': -64, 'download': 252, 'upload': 360, 'interferencia': 0},
        {'id': 4, 'dbm': -69, 'download': 216, 'upload': 360, 'interferencia': 0},
        {'id': 5, 'dbm': -52, 'download': 72, 'upload': 32, 'interferencia': 0},
        {'id': 6, 'dbm': -61, 'download': 504, 'upload': 576, 'interferencia': 0},
        {'id': 7, 'dbm': -54, 'download': 111, 'upload': 43, 'interferencia': 0},
        {'id': 8, 'dbm': -54, 'download': 91, 'upload': 36, 'interferencia': 0},
        {'id': 9, 'dbm': -60, 'download': 90, 'upload': 44, 'interferencia': 0},
        {'id': 10, 'dbm': -56, 'download': 131, 'upload': 81, 'interferencia': 0},
        {'id': 11, 'dbm': -51, 'download': 741, 'upload': 741, 'interferencia': 0},
        {'id': 12, 'dbm': -62, 'download': 585, 'upload': 585, 'interferencia': 0},
        {'id': 13, 'dbm': -60, 'download': 585, 'upload': 585, 'interferencia': 0},
        {'id': 14, 'dbm': -52, 'download': 823, 'upload': 823, 'interferencia': 0},
        {'id': 15, 'dbm': -62, 'download': 613, 'upload': 613, 'interferencia': 0},
        {'id': 16, 'dbm': -52, 'download': 823, 'upload': 823, 'interferencia': 0},
        {'id': 17, 'dbm': -71, 'download': 424, 'upload': 424, 'interferencia': 0},
        {'id': 18, 'dbm': -68, 'download': 485, 'upload': 485, 'interferencia': 0},
        {'id': 19, 'dbm': -58, 'download': 585, 'upload': 585, 'interferencia': 0},
    ]
    
    # Adicionei um zero para a coluna 'interferencia' que não estava na imagem,
    # para corresponder ao nosso modelo.

    # Documentação: Atualizamos o contexto para enviar os novos dados de sinais.
    # A chave agora é 'dados_sinais'.
    context = {
        'dados_sinais': sinais_mock,
    }

    return render(request, 'dashboard/index.html', context)
'''
def primeiro_andar_view(request):
    """
    View para a página do primeiro andar.
    
    Busca os dados estáticos do primeiro andar e os envia para o template.
    O contexto 'dados' conterá a lista de medições.
    """
    context = {
        'titulo': 'Primeiro Andar',
        'dados': dados_primeiro_andar,
    }
    return render(request, 'dashboard/primeiro_andar.html', context)

def segundo_andar_view(request):
    """
    View para a página do segundo andar.
    
    Busca os dados estáticos do segundo andar e os envia para o template.
    O contexto 'dados' conterá a lista de medições.
    """
    context = {
        'titulo': 'Segundo Andar',
        'dados': dados_segundo_andar,
    }
    return render(request, 'dashboard/segundo_andar.html', context)