# 5th-semester/desenvolvimento-de-projeto-1/desenvolvimento-de-projeto-1-interface-projeto/dashboard/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .dados_estaticos import dados_primeiro_andar, dados_segundo_andar
from .models import DadosSinais
import math


def _compute_heatcolor(dbm: float, min_dbm: float = -90.0, max_dbm: float = -40.0) -> str:
    """Map a dbm value to a hex color between red (weak) and green (strong)."""
    try:
        val = (dbm - min_dbm) / (max_dbm - min_dbm)
    except Exception:
        val = 0.0
    val = max(0.0, min(1.0, val))
    # green (strong) and red (weak)
    r_strong, g_strong, b_strong = 22, 163, 74   # green-ish
    r_weak, g_weak, b_weak = 239, 68, 68        # red-ish
    r = int(r_strong * val + r_weak * (1 - val))
    g = int(g_strong * val + g_weak * (1 - val))
    b = int(b_strong * val + b_weak * (1 - val))
    return f"#{r:02x}{g:02x}{b:02x}"


def _enrich_lista(dados):
    enriched = []
    for entrada in dados:
        # copy original data and normalize types
        item = dict(entrada)
        try:
            dbm = float(entrada.get('dbm', 0))
        except Exception:
            dbm = 0.0
        interfer = entrada.get('interferencia', 0)
        try:
            interfer = float(interfer)
        except Exception:
            # keep original if cannot convert
            pass
        item['dbm'] = dbm
        item['interferencia'] = interfer
        item['heatcolor'] = _compute_heatcolor(dbm)
        enriched.append(item)
    return enriched


def primeiro_andar_view(request):
    """
    View para a página do primeiro andar.
    Envia dados enriquecidos (com 'interferencia' numérica e 'heatcolor') para o template.
    """
    context = {
        'titulo': 'Primeiro Andar',
        'dados_primeiro_andar': _enrich_lista(dados_primeiro_andar),
    }
    return render(request, 'dashboard/primeiro_andar.html', context)


def segundo_andar_view(request):
    """
    View para a página do segundo andar.
    Envia dados enriquecidos (com 'interferencia' numérica e 'heatcolor') para o template.
    """
    context = {
        'titulo': 'Segundo Andar',
        'dados_segundo_andar': _enrich_lista(dados_segundo_andar),
    }
    return render(request, 'dashboard/segundo_andar.html', context)


# API endpoint to provide summary data for charts
def api_summary(request):
    """Retorna JSON com todos os sinais no formato { sinais: [ {id, dbm, download, upload, interferencia, comodo}, ... ] }.
    Prioriza dados do banco; se não houver dados, usa dados_estaticos como fallback.
    Todos os campos numéricos são validados e claMPados para evitar NaN/Infinity e valores extremos.
    """
    sinais = []

    def _to_float_safe(v, default=0.0):
        try:
            n = float(v)
            if not math.isfinite(n):
                return default
            return n
        except Exception:
            return default

    def _clamp(v, mn, mx):
        return max(mn, min(mx, v))

    def _sanitize(item):
        dbm = _to_float_safe(item.get('dbm', 0.0), 0.0)
        download = _to_float_safe(item.get('download', 0.0), 0.0)
        upload = _to_float_safe(item.get('upload', 0.0), 0.0)
        interfer = _to_float_safe(item.get('interferencia', 0.0), 0.0)
        # clamp to sensible ranges
        dbm = _clamp(dbm, -120.0, 0.0)
        download = _clamp(download, 0.0, 2000.0)
        upload = _clamp(upload, 0.0, 2000.0)
        interfer = _clamp(interfer, 0.0, 100.0)
        return {
            'id': item.get('id'),
            'dbm': dbm,
            'download': download,
            'upload': upload,
            'interferencia': interfer,
            'comodo': item.get('comodo')
        }

    qs = DadosSinais.objects.select_related('comodo').all()
    if qs.exists():
        for s in qs:
            sinais.append(_sanitize({
                'id': s.id,
                'dbm': float(s.dbm),
                'download': float(s.download),
                'upload': float(s.upload),
                'interferencia': float(s.interferencia),
                'comodo': s.comodo.nome if s.comodo else None,
            }))
    else:
        # fallback to static lists
        for s in dados_segundo_andar:
            item = dict(s)
            item['comodo'] = 'Segundo Andar'
            sinais.append(_sanitize(item))
        for s in dados_primeiro_andar:
            item = dict(s)
            item['comodo'] = 'Primeiro Andar'
            sinais.append(_sanitize(item))

    return JsonResponse({'sinais': sinais}, safe=True)
