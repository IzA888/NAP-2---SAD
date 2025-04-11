from celery.schedules import crontab

from Financas import apps

apps.conf.beat_schedule = {
    'exportar-dados-diarios': {
        'task': 'financas.tasks.exportar_dados_diarios',
        'schedule': crontab(hour=23, minute=55),  # Executa todo dia às 23:55
    },
}