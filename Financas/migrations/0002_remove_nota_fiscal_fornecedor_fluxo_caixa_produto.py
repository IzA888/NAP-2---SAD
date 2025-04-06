# Generated by Django 4.1.13 on 2025-04-06 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Financas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nota_fiscal',
            name='fornecedor',
        ),
        migrations.AddField(
            model_name='fluxo_caixa',
            name='produto',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Financas.produto'),
            preserve_default=False,
        ),
    ]
