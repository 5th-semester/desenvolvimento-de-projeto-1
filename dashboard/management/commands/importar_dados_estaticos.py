from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.models import AnaliseRede, Comodo, DadosSinais
from dashboard import dados_estaticos


class Command(BaseCommand):
    help = 'Importa dados estáticos do arquivo dashboard/dados_estaticos.py e popula o banco.'

    def handle(self, *args, **options):
        with transaction.atomic():
            analise, created = AnaliseRede.objects.get_or_create(
                nome_cliente='Importação Dados Estáticos',
                defaults={'endereco': 'Importado'}
            )

            total_sinais_criados = 0

            # Criar apenas dois cômodos: Primeiro Andar e Segundo Andar
            comodo_segundo, _ = Comodo.objects.get_or_create(
                analise_rede=analise,
                nome='Segundo Andar',
                defaults={'descricao': 'Dados do segundo andar importados'}
            )

            comodo_primeiro, _ = Comodo.objects.get_or_create(
                analise_rede=analise,
                nome='Primeiro Andar',
                defaults={'descricao': 'Dados do primeiro andar importados'}
            )

            # Importar sinais do segundo andar para o cômodo correspondente
            for entrada in dados_estaticos.dados_segundo_andar:
                DadosSinais.objects.create(
                    comodo=comodo_segundo,
                    dbm=float(entrada.get('dbm', 0)),
                    download=float(entrada.get('download', 0)),
                    upload=float(entrada.get('upload', 0)),
                    interferencia=float(entrada.get('interferencia', 0))
                )
                total_sinais_criados += 1

            # Importar sinais do primeiro andar para o cômodo correspondente
            for entrada in dados_estaticos.dados_primeiro_andar:
                DadosSinais.objects.create(
                    comodo=comodo_primeiro,
                    dbm=float(entrada.get('dbm', 0)),
                    download=float(entrada.get('download', 0)),
                    upload=float(entrada.get('upload', 0)),
                    interferencia=float(entrada.get('interferencia', 0))
                )
                total_sinais_criados += 1

        self.stdout.write(self.style.SUCCESS(
            f"Importação concluída: 2 cômodos (Primeiro Andar, Segundo Andar), {total_sinais_criados} sinais importados."))
