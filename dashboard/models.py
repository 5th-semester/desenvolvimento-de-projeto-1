# dashboard/models.py

from django.db import models

class AnaliseRede(models.Model):
    """
    Modelo principal para armazenar uma análise completa de uma rede.
    Funciona como um "relatório" geral.
    """
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data da Análise")
    nome_cliente = models.CharField(max_length=150, verbose_name="Nome do Cliente")
    endereco = models.CharField(max_length=250, verbose_name="Endereço")
    
    def __str__(self):
        return f"Análise para {self.nome_cliente} em {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Análise de Rede"
        verbose_name_plural = "Análises de Rede"

class Comodo(models.Model):
    """
    Modelo para armazenar os cômodos associados a uma análise.
    Cada cômodo terá seus próprios dados de sinal.
    """
    analise_rede = models.ForeignKey(AnaliseRede, on_delete=models.CASCADE, related_name="comodos")
    nome = models.CharField(max_length=100, verbose_name="Nome do Cômodo")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição/Problemas")
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cômodo"
        verbose_name_plural = "Cômodos"

class DadosSinais(models.Model):
    """
    Modelo para armazenar os dados técnicos do sinal medido em um cômodo específico.
    Agora um cômodo pode possuir vários sinais (relação One-to-Many).
    """
    comodo = models.ForeignKey(Comodo, on_delete=models.CASCADE, related_name="sinais")
    dbm = models.FloatField(verbose_name="Potência (dBm)")
    download = models.FloatField(verbose_name="Velocidade de Download (Mbps)")
    upload = models.FloatField(verbose_name="Velocidade de Upload (Mbps)")
    interferencia = models.FloatField(verbose_name="Interferência (%)")

    def __str__(self):
        return f"Sinal para: {self.comodo.nome} (ID do Cômodo: {self.comodo.id})"

    class Meta:
        verbose_name = "Dado de Sinal"
        verbose_name_plural = "Dados de Sinais"