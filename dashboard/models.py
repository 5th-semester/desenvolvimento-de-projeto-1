# dashboard/models.py

from django.db import models
import statistics

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

    # --- Novos métodos úteis para dashboards / gráficos ---
    def get_all_sinais(self):
        """Retorna QuerySet com todos os DadosSinais relacionados a esta análise."""
        return DadosSinais.objects.filter(comodo__analise_rede=self)

    @staticmethod
    def _classify_measurement(dbm: float, download: float, interferencia: float):
        """Classifica uma medição e retorna (status, [motivos]).
        Regras simples (ajustáveis):
          - boa: dbm >= -60 e download >= 100 e interferencia <= 50
          - ruim: caso contrário
        Motivos detectados: sinal muito fraco / sinal fraco / baixa velocidade / alta interferência / condições normais
        """
        reasons = []
        try:
            dbm = float(dbm)
        except Exception:
            dbm = 0.0
        try:
            download = float(download)
        except Exception:
            download = 0.0
        try:
            interfer = float(interferencia)
        except Exception:
            interfer = 0.0

        if dbm < -70:
            reasons.append('Sinal muito fraco')
        elif dbm < -65:
            reasons.append('Sinal fraco')

        if download < 50:
            reasons.append('Baixa velocidade de download')

        if interfer > 50:
            reasons.append('Alta interferência')

        if not reasons:
            reasons.append('Condições normais')

        status = 'boa' if (dbm >= -60 and download >= 100 and interfer <= 50) else 'ruim'
        return status, reasons

    def get_status_counts(self):
        """Retorna um dict com contagem de sinais {'boa': X, 'ruim': Y}."""
        counts = {'boa': 0, 'ruim': 0}
        for s in self.get_all_sinais().iterator():
            status, _ = self._classify_measurement(s.dbm, s.download, s.interferencia)
            counts[status] = counts.get(status, 0) + 1
        return counts

    def get_reasons_count(self):
        """Retorna um dict com contagem agregada de motivos (strings)"""
        reasons = {}
        for s in self.get_all_sinais().iterator():
            _, rs = self._classify_measurement(s.dbm, s.download, s.interferencia)
            for r in rs:
                reasons[r] = reasons.get(r, 0) + 1
        return reasons

    def avg_dbm_per_comodo(self):
        """Retorna dict {comodo_nome: avg_dbm}"""
        result = {}
        for c in self.comodos.all():
            vals = [s.dbm for s in c.sinais.all() if s.dbm is not None]
            result[c.nome] = statistics.mean(vals) if vals else None
        return result

    def get_bad_signals(self):
        """Retorna lista de sinais classificados como 'ruim' com detalhes para exibir no dashboard."""
        bad = []
        for s in self.get_all_sinais().iterator():
            status, rs = self._classify_measurement(s.dbm, s.download, s.interferencia)
            if status == 'ruim':
                bad.append({
                    'comodo': s.comodo.nome,
                    'dbm': s.dbm,
                    'download': s.download,
                    'interferencia': s.interferencia,
                    'motivos': rs,
                })
        return bad

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

    # --- Métodos úteis para gráficos ---
    def avg_dbm(self):
        """Média do dbm dos sinais deste cômodo (ou None)."""
        vals = [s.dbm for s in self.sinais.all() if s.dbm is not None]
        return statistics.mean(vals) if vals else None

    def status_summary(self):
        """Retorna contagem de sinais bons/ruins apenas para este cômodo."""
        counts = {'boa': 0, 'ruim': 0}
        for s in self.sinais.all():
            status, _ = AnaliseRede._classify_measurement(s.dbm, s.download, s.interferencia)
            counts[status] = counts.get(status, 0) + 1
        return counts

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