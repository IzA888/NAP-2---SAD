from datetime import datetime
from celery import shared_task
from django.core.management import call_command


@shared_task
def exportar_dados_diarios():
    print(f"Iniciando exportação de dados em {datetime.now()}")
    call_command('exportar_dados_csv')