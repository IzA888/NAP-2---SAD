# Generated by Django 5.2 on 2025-04-10 18:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Financas', '0008_alter_fluxo_caixa_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cpf_cnpj', models.CharField(max_length=20, unique=True)),
                ('telefone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('endereco', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='produto',
            name='categoria',
        ),
        migrations.RemoveField(
            model_name='produto',
            name='data_cadastro',
        ),
        migrations.AddField(
            model_name='produto',
            name='codigo',
            field=models.CharField(default=0, max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produto',
            name='estoque',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produto',
            name='nome',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='produto',
            name='descricao',
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_venda', models.DateTimeField(auto_now_add=True)),
                ('forma_pagamento', models.CharField(choices=[('dinheiro', 'Dinheiro'), ('cartao', 'Cartão'), ('pix', 'PIX'), ('boleto', 'Boleto')], max_length=20)),
                ('desconto', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('observacoes', models.TextField(blank=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Financas.cliente')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemVenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Financas.produto')),
                ('venda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='Financas.venda')),
            ],
        ),
        migrations.DeleteModel(
            name='Vendas',
        ),
    ]
