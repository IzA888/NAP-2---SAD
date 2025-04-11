from django.urls import path
from django.conf.urls.static import static
from GestaodeFinancas import settings
from . import views

app_name = 'financas'  # Em minúsculas
urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('configuracoes/', views.configuracoes_vendas, name='dashboard_configuracoes'),
    # Produtos
    path('estoques/', views.ProdutoListView.as_view(), name='listar_produtos'),
    path('estoques/novo/', views.ProdutoCreateView.as_view(), name='adicionar_produto'),
    path('estoques/editar/<int:pk>/', views.ProdutoUpdateView.as_view(), name='editar_produto'),
    path('estoques/excluir/<int:pk>/', views.ProdutoDeleteView.as_view(), name='excluir_produto'),
    # Vendas
    path('vendas/nova/', views.NovaVendaView.as_view(), name='nova_venda'),
    path('vendas/busca_produto/<int:produto_id>/', views.BuscaProdutoView.as_view(), name='busca_produto'),
    path('vendas/comparativo_vendas/', views.comparar_periodos, name='vendas_comparativo_vendas'),
    path('vendas/relatorios/', views.relatorios_vendas, name='vendas_relatorios'),
    
    # Fluxo de Caixa
    path('fluxo_caixa/', views.FluxoCaixaView.as_view(), name='fluxo_caixa'),
    
    # Receitas
    path('receitas/despesas/', views.despesas, name='receitas_despesas'),
    path('receitas/saldo/', views.saldo, name='receitas_saldo'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
