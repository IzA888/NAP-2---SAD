# Generated by Django 5.2 on 2025-04-10 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Financas', '0007_alter_fluxo_caixa_options_alter_transacao_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fluxo_caixa',
            options={'ordering': ['ordem'], 'verbose_name_plural': 'Fluxos de Caixa'},
        ),
    ]
