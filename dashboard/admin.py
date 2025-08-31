# dashboard/admin.py

from django.contrib import admin
# Documentação: Agora podemos importar todos os nossos modelos,
# pois eles estão corretamente definidos no models.py
from .models import AnaliseRede, Comodo, DadosSinais

# Documentação: O comando admin.site.register() torna um modelo
# visível e gerenciável na interface de administração do Django.
admin.site.register(AnaliseRede)
admin.site.register(Comodo)
admin.site.register(DadosSinais)