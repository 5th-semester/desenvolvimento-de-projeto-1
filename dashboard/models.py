# Documentação: Importa as ferramentas de modelo do Django.
from django.db import models

# Documentação: Define o modelo para uma análise de rede.
# Cada vez que uma análise é feita, um novo registro deste tipo será criado.
class AnaliseRede(models.Model):
    # Documentação: Campo para armazenar a data e hora em que a análise foi realizada.
    # auto_now_add=True garante que este campo seja preenchido automaticamente
    # com o momento da criação.
    timestamp = models.DateTimeField(auto_now_add=True)

    # Documentação: SSID (nome) da rede WiFi analisada.
    # CharField é usado para textos de comprimento limitado. max_length é obrigatório.
    ssid = models.CharField(max_length=100)

    # Documentação: Intensidade do sinal em dBm (geralmente um valor negativo).
    # IntegerField é para números inteiros.
    intensidade_sinal = models.IntegerField()

    # Documentação: Canal em que a rede está operando.
    canal = models.IntegerField()

    # Documentação: Campo de texto para armazenar um diagnóstico gerado pelo backend.
    # TextField é usado para textos longos, sem limite definido.
    diagnostico = models.TextField()

    # Documentação: Campo de texto para armazenar as soluções sugeridas.
    solucoes_sugeridas = models.TextField()

    # Documentação: O método __str__ define como o objeto será exibido,
    # por exemplo, na área de administração do Django.
    def __str__(self):
        return f"Análise da rede {self.ssid} em {self.timestamp}"