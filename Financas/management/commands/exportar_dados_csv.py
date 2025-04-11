import csv
from datetime import datetime, timedelta
from django.utils import timezone
import glob
import os
from django.core.management.base import BaseCommand
from Financas.models import Fluxo_Caixa, Produto, Transacao, Venda
from GestaodeFinancas import settings


class Command(BaseCommand):
    help = 'Exporta dados do banco para arquivos CSV'

    def handle(self, *args, **options):
        # Diretório para salvar os arquivos
        export_dir = settings.DATA_EXPORT_DIR
        os.makedirs(export_dir, exist_ok=True)
        
        # Data atual para nome do arquivo
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Exportar cada modelo
        self.export_model(Transacao, f'{export_dir}/transacoes_{date_str}.csv')
        self.export_model(Produto, f'{export_dir}/produtos_{date_str}.csv')
        self.export_model(Venda, f'{export_dir}/vendas_{date_str}.csv')
        self.export_model(Fluxo_Caixa, f'{export_dir}/fluxo_caixa_{date_str}.csv')

        clean_old_exports(export_dir, settings.DATA_EXPORT_RETENTION_DAYS)
        
        self.stdout.write(self.style.SUCCESS('Dados exportados com sucesso!'))

    def export_model(self, model, filepath):
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Escrever cabeçalho
            field_names = [field.name for field in model._meta.fields]
            writer.writerow(field_names)
            
            # Escrever dados
            for obj in model.objects.all():
                row = [getattr(obj, field) for field in field_names]
                writer.writerow(row)
        


def clean_old_exports(export_dir, days_to_keep=7):
    cutoff = timezone.now() - timedelta(days=days_to_keep)
    for file in glob.glob(f'{export_dir}/*.csv'):
        if os.path.getmtime(file) < cutoff.timestamp():
            os.remove(file)
