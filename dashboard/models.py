from django.db import models

# Create your models here.

class DadosSinais(models.Model):
    """
    Modelo para armazenar dados de sinais de rede, como potência,
    velocidades de download/upload e interferência.
    """
    id = models.IntegerField(primary_key=True, unique=True, verbose_name="ID")
    dbm = models.FloatField()
    download = models.FloatField()
    upload = models.FloatField()
    interferencia = models.FloatField()

    def __str__(self):
        """
        Retorna uma representação em string do objeto, útil no admin do Django.
        """
        return f"Sinal ID: {self.id}"

    class Meta:
        """
        Metadados do modelo para configurar o comportamento no admin do Django.
        """
        verbose_name = "Dado de Sinal"
        verbose_name_plural = "Dados de Sinais"