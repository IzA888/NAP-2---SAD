import csv
from datetime import datetime, timedelta
import glob
import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils import timezone

from GestaodeFinancas import settings 
from .models import MetricasFinanceiras, Transacao, Fluxo_Caixa, Venda, Produto, ItemVenda
from .forms import ProdutoForm, VendaForm, ItemVendaForm
import matplotlib.pyplot as plt
from io import BytesIO
from Financas import models
import base64
import json
from django.core.cache import cache

class DashboardView(View):
    menu_ativo = 'dashboard'
    
    def get_menu_context(self):
        """Retorna o contexto do menu"""
        return {
        'menu_ativo': self.menu_ativo,
        'menu_items': [
            {
                'nome': 'Vendas', 
                'subitens': [
                    {'nome': 'Comparativo de Vendas', 'url': 'financas:vendas_comparativo_vendas'},
                    {'nome': 'Relatórios', 'url': 'financas:vendas_relatorios'},
                ],
                'url': ''  # URL principal para Vendas
            },
            {
                'nome': 'Fluxo de Caixa', 
                'subitens': [],
                'url': 'financas:fluxo_caixa'  # URL direta
            },
            {
                'nome': 'Receitas', 
                'subitens': [
                    {'nome': 'Despesas', 'url': 'financas:receitas_despesas'},
                    {'nome': 'Saldo', 'url': 'financas:receitas_saldo'}
                ],
                'url': ''  # URL principal para Receitas
            },
            {
                'nome': 'Estoque', 
                'subitens': [
                    {'nome': 'Listar Produtos', 'url': 'financas:estoques_listar_produtos'},
                ],
                'url': ''  # URL principal para Estoque
            },
            {
                'nome': 'Configurações',
                'subitens': [
                    {'nome': 'Configurações' , 'url': 'financas:dashboard_configuracoes'},
                ],
            },
        ],
    }
    
    
    def get_fluxo_caixa_data(self):
        """Obtém e processa dados do fluxo de caixa dos últimos 7 dias"""
        # Calcula a data de 1 semana atrás
        uma_semana_atras = timezone.now() - timedelta(days=7)
        
        # Filtra os registros dos últimos 7 dias e ordena
        fluxos = Fluxo_Caixa.objects.filter(
            data__gte=uma_semana_atras
        ).order_by('data')
        
        # Extrai dias e valores
        dias = [f.data.strftime('%DD/%MM') for f in fluxos]  # Formato DD/MM
        valores = []
        
        for f in fluxos.only('valor'):
            try:
                valores.append(float(f.valor))
            except (TypeError, ValueError):
                valores.append(0.0)
        
        # Gera o gráfico
        grafico = self.gerar_grafico_fluxo_caixa(dias, valores)
        
        return {
            'dados_combinados': list(zip(dias, valores)),
            'grafico': grafico,
            'dias': dias,
            'valores': valores,
            'total': sum(valores),
            'periodo': f"{uma_semana_atras.strftime('%DD/%MM/%YY')} a {timezone.now().strftime('%d/%m/%Y')}"
        }

    def gerar_grafico_fluxo_caixa(self, dias, valores):
        """Gera gráfico otimizado para os últimos 7 dias"""
        # Configurações do estilo
        plt.style.use('seaborn-v0_8-darkgrid')
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.titlepad'] = 15
        
        # Cria figura otimizada
        fig, ax = plt.subplots(figsize=(10, 4), dpi=90)
        
        # Cores e estilos
        cor_barras = '#4e79a7'
        cor_texto = '#2e2e2e'
        
        # Gráfico de barras
        bars = ax.bar(dias, valores, color=cor_barras, alpha=0.8, width=0.6)
        
        # Rótulos nas barras
        max_valor = max(valores) if valores else 0
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2., 
                height + (max_valor * 0.02 if max_valor > 0 else 0.02),
                f'R$ {height:,.0f}',
                ha='center', 
                va='bottom', 
                fontsize=9,
                color=cor_texto
            )
        
        # Configurações do eixo Y
        ax.set_ylim(0, max_valor * 1.2 if max_valor > 0 else 1)
        ax.yaxis.set_major_formatter('R$ {x:,.0f}')
        
        # Títulos e rótulos
        ax.set_title('Fluxo de Caixa - Últimos 7 Dias', fontweight='bold')
        ax.set_xlabel('Data')
        ax.set_ylabel('Valor (R$)')
        
        # Formatação dos eixos
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.yticks(fontsize=9)
        
        # Remove bordas desnecessárias
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
        
        # Grid mais sutil
        ax.grid(axis='y', linestyle=':', alpha=0.4)
        
        # Ajuste de layout
        plt.tight_layout()
        
        # Salva em arquivo (opcional)
        
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'static'), exist_ok=True)
        filepath = os.path.join(settings.MEDIA_ROOT, 'fluxo_7dias.png')
        plt.savefig(filepath, format='png', dpi=90, bbox_inches='tight')
        

        plt.close(filepath)  # Fecha a figura para liberar memória


    
    def get_transacoes_recentes(self):
        """Obtém transações recentes ou dados mockados"""
        transacoes = Transacao.objects.all().order_by('-data')[:5] or [
            {'data': '30/06/2023', 'descricao': 'Saldo Inicial', 'valor': '15.000,00', 'status': 'pago'},
            {'data': '09/07/2023', 'descricao': 'Pagamento Fornecedora Nacional', 'valor': '5.000,00', 'status': 'pago'},
            {'data': '14/07/2023', 'descricao': 'Recebimento João Silva', 'valor': '2.000,00', 'status': 'recebido'},
            {'data': '19/07/2023', 'descricao': 'Recebimento Maria Oliveira', 'valor': '1.500,00', 'status': 'recebido'},
            {'data': '09/08/2023', 'descricao': 'Pagamento Distribuidora Exportação', 'valor': '3.500,00', 'status': 'pago'},
        ]
        return transacoes
    
    def get_transacoes_pendentes(self):
        """Obtém transações pendentes"""
        hoje = timezone.now().date()
        return [
            {
                'contraparte': 'Pedro Santos',
                'descricao': 'Parcela 1 - Vencimento 04/09',
                'valor': '3.000,00',
                'dias_atraso': 583,
                'tipo': 'receita'
            },
            {
                'contraparte': 'Fornecedora Nacional Ltda',
                'descricao': 'Parcela 1 - Vencimento 09/09',
                'valor': '4.200,00',
                'dias_atraso': 578,
                'tipo': 'despesa'
            },
            {
                'contraparte': 'João Silva',
                'descricao': 'Parcela 3 - Vencimento 14/09',
                'valor': '2.000,00',
                'dias_atraso': 573,
                'tipo': 'receita'
            }
        ]
    
    def get(self, request):
        # Obter todos os dados necessários
        menu_context = self.get_menu_context()
        fluxo_caixa_data = self.get_fluxo_caixa_data()
        
        context = {
            'metrica': MetricasFinanceiras.obter_metricas(),
            'transacoes': self.get_transacoes_recentes(),
            'transacoes_pendentes': self.get_transacoes_pendentes(),
            'grafic': self.get_fluxo_caixa_data(),
            **menu_context,
            **fluxo_caixa_data
        }
        
        return render(request, 'dashboard/index.html', context)
    
class NovaVendaView(View):
    def get(self, request):
        form_venda = VendaForm()
        form_item = ItemVendaForm()
        produtos = Produto.objects.all()
        
        context = {
            'form_venda': form_venda,
            'form_item': form_item,
            'produtos_json': json.dumps([{
                'id': p.id,
                'nome': p.nome,
                'preco': float(p.preco),
                'estoque': p.estoque
            } for p in produtos])
        }
        return render(request, 'vendas/nova_venda.html', context)
    
    def post(self, request):
        data = json.loads(request.body)
        
        # Criar a venda
        venda = Venda.objects.create(
            cliente_id=data['cliente_id'],
            usuario=request.user,
            forma_pagamento=data['forma_pagamento'],
            desconto=float(data['desconto']),
            valor_total=float(data['valor_total']),
            observacoes=data['observacoes']
        )
        
        # Adicionar itens
        for item in data['itens']:
            produto = get_object_or_404(Produto, pk=item['produto_id'])
            ItemVenda.objects.create(
                venda=venda,
                produto=produto,
                quantidade=int(item['quantidade']),
                preco_unitario=float(item['preco_unitario']),
                subtotal=float(item['subtotal'])
            )
            # Atualizar estoque
            produto.estoque -= int(item['quantidade'])
            produto.save()
    
        return JsonResponse({'success': True, 'venda_id': venda.id})

class BuscaProdutoView(View):
    def get(self, request, produto_id):
        produto = get_object_or_404(Produto, pk=produto_id)
        data = {
            'id': produto.id,
            'nome': produto.nome,
            'preco': float(produto.preco),
            'estoque': produto.estoque
        }
        return JsonResponse(data)
    

class ProdutoListView(ListView):
    model = Produto
    template_name = 'estoques/listar_produtos.html'
    context_object_name = 'produtos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        busca = self.request.GET.get('busca')
        
        if busca:
            queryset = queryset.filter(
                models.Q(nome__icontains=busca) |
                models.Q(codigo__icontains=busca) |
                models.Q(descricao__icontains=busca)
            )
        
        return queryset.order_by('nome')

class ProdutoCreateView(SuccessMessageMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'estoques/adicionar_produto.html'
    success_url = reverse_lazy('listar_produtos')
    success_message = "Produto adicionado com sucesso!"
   

class ProdutoUpdateView(SuccessMessageMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'estoques/adicionar_produto.html'
    success_url = reverse_lazy('estoques:listar_produtos')
    success_message = "Produto atualizado com sucesso!"

class ProdutoDeleteView(DeleteView):
    model = Produto
    success_url = reverse_lazy('estoques:listar_produtos')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Produto removido com sucesso!")
        return super().delete(request, *args, **kwargs)

# Vendas

def relatorios_vendas(request):
    return render(request, 'vendas/relatorios.html', {'menu_ativo': 'vendas'})

def configuracoes_vendas(request):
    return render(request, 'vendas/configuracoes.html', {'menu_ativo': 'vendas'})

# Fluxo de Caixa
class FluxoCaixaView(DashboardView, View):
    menu_ativo = 'fluxo_caixa'
    
    def get(self, request):
        return render(request, 'dashboard/fluxo_caixa.html', self.get_menu_context())

# Receitas
def despesas(request):
    return render(request, 'receitas/despesas.html', {'menu_ativo': 'receitas'})

def saldo(request):
    return render(request, 'receitas/saldo.html', {'menu_ativo': 'receitas'})


def encontrar_arquivo_mais_recente(padrao):
    """Encontra o arquivo mais recente que corresponde ao padrão"""
    arquivos = glob.glob(padrao)
    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo encontrado com o padrão: {padrao}")
    
    # Ordena por data de modificação (mais recente primeiro)
    arquivos.sort(key=os.path.getmtime, reverse=True)
    return arquivos[0]

def comparar_periodos(request):
    cache_key = f"comparativo_{timezone.now().date()}"
    dados = cache.get(cache_key)

    if not dados:
        hoje = timezone.now().date()
        uma_semana_atras = hoje - timedelta(days=7)
        seis_meses_atras = hoje - timedelta(days=180)

        # Função para converter string para float com segurança
        def to_float(value, default=0.0):
            try:
                return float(value)
            except (TypeError, ValueError):
                return default

        # Função para processar dados do CSV
        def processar_csv(arquivo, data_inicio, data_fim):
            vendas_total = 0.0
            quantidade = 0
            saldo = 0.0  # Adicione cálculo específico para fluxo de caixa
            
            with open(arquivo, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        data_venda = datetime.strptime(row['data_venda'], '%Y-%m-%d').date()
                        if data_inicio <= data_venda <= data_fim:
                            valor = to_float(row['valor'])
                            vendas_total += valor
                            quantidade += 1
                            # Ajuste para fluxo de caixa
                            if 'tipo' in row:
                                saldo += valor if row['tipo'].lower() == 'entrada' else -valor
                    except (KeyError, ValueError):
                        continue
    
                return {
                    'total_vendas': vendas_total,
                    'quantidade': quantidade,
                    'saldo': saldo
                }
        # Encontra automaticamente os arquivos mais recentes
        try:
            caminho_vendas = encontrar_arquivo_mais_recente('Financas/exports/vendas_*.csv')
            caminho_fluxo = encontrar_arquivo_mais_recente('Financas/exports/fluxo_caixa_*.csv')
        except FileNotFoundError as e:
            return JsonResponse({'erro': str(e)}, status=404)

        # Processar dados para os períodos
        dados_semana = {
            'vendas': processar_csv(caminho_vendas, uma_semana_atras, hoje),
            'fluxo_caixa': processar_csv(caminho_fluxo, uma_semana_atras, hoje)
        }
        
        dados_seis_meses = {
            'vendas': processar_csv(caminho_vendas, seis_meses_atras, hoje),
            'fluxo_caixa': processar_csv(caminho_fluxo, seis_meses_atras, hoje)
        }

        # Cálculo de variação percentual
        def calcular_variacao(atual, anterior):
            if anterior == 0:
                return 0
            return ((atual - anterior) / anterior) * 100

        # Comparativo entre períodos
        comparativo = {
            'vendas': {
                'variacao_valor': dados_semana['vendas']['total_vendas'] - dados_seis_meses['vendas']['total_vendas'],
                'variacao_percentual': calcular_variacao(
                    dados_semana['vendas']['total_vendas'],
                    dados_seis_meses['vendas']['total_vendas']
                ),
                'variacao_quantidade': dados_semana['vendas']['quantidade'] - dados_seis_meses['vendas']['quantidade']
            },
            'fluxo_caixa': {
                'variacao_saldo': dados_semana['fluxo_caixa']['total_vendas'] - dados_seis_meses['fluxo_caixa']['total_vendas'],
                'variacao_percentual': calcular_variacao(
                    dados_semana['fluxo_caixa']['total_vendas'],
                    dados_seis_meses['fluxo_caixa']['total_vendas']
                )
            }
        }

        dados = {
            'periodos': {
                'uma_semana': {
                    'inicio': uma_semana_atras,
                    'fim': hoje
                },
                'seis_meses': {
                    'inicio': seis_meses_atras,
                    'fim': hoje
                }
            },
            'dados_semana': dados_semana,
            'dados_seis_meses': dados_seis_meses,
            'comparativo': comparativo
        }

        cache.set(cache_key, dados, timeout=86400)  # Cache por 24h

    return render(request, 'vendas/comparativo_vendas.html', dados)