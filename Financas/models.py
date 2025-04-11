from itertools import count
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Sum, F, Count

# Create your models here.
User = get_user_model()

class Produto(models.Model):
    codigo = models.CharField('Código', max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField('Estoque Mínimo', default=0)
    descricao = models.TextField('Descrição', blank=True)
    data_cadastro = models.DateTimeField('Data de Cadastro', default=timezone.now)
    ultima_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} (Estoque: {self.estoque})"

    def get_absolute_url(self):
        return reverse('listar_produtos')

    def situacao_estoque(self):
        if self.estoque <= 0:
            return 'Esgotado'
        elif self.estoque <= self.estoque_minimo:
            return 'Abaixo do mínimo'
        return 'Disponível'
    def data_cadastro_formatada(self):
        return self.data_cadastro.strftime("%DD/%MM/%YY, %H:%M:%S")

    def ultima_atualizacao_formatada(self):
        return self.ultima_atualizacao.strftime("%DD/%MM/%YY, %H:%M:%S")
 
class Fluxo_Caixa(models.Model):
    data = models.DateField()
    descricao = models.CharField(max_length=100)
    total_vendas = models.DecimalField(max_digits=10, decimal_places=2)
    total_despesas = models.DecimalField(max_digits=10, decimal_places=2)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('saida', 'Saída')])
    saldo_acumulado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mes = models.CharField(max_length=3)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    ordem = models.IntegerField()

    class Meta:
        verbose_name_plural = "Fluxos de Caixa"
        ordering = ['ordem']

    def __str__(self):
        return f"{self.mes}: R$ {self.valor}"
    
    @classmethod
    def saldo_por_periodo(cls, inicio, fim):
        return cls.objects.filter(
            data__range=(inicio, fim)
        ).aggregate(
            total_entradas=Sum('total_vendas'),
            total_saidas=Sum('total_despesas'),
            saldo=Sum(F('total_vendas') - F('total_despesas'))
        )

class Nota_Fiscal(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    data_emissao = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    imposto = models.DecimalField(max_digits=10, decimal_places=2)
    

class Imposto(models.Model):
    tipo = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_emissao = models.DateField()
    status = models.CharField(max_length=20, choices=[('pago', 'Pago'), ('pendente', 'Pendente')])


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    endereco = models.TextField()

    def __str__(self):
        return self.nome


class Venda(models.Model):
    FORMA_PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('cartao', 'Cartão'),
        ('pix', 'PIX'),
        ('boleto', 'Boleto'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    data_venda = models.DateTimeField('Data_da_venda', auto_now_add=True)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"Venda #{self.id} - {self.cliente.nome}"
    
    @classmethod
    def total_por_periodo(cls, inicio, fim):
        return cls.objects.filter(
            data_venda__range=(inicio, fim)
        ).aggregate(
            total_vendas=Sum('valor_total'),
            quantidade=Count('id')
        )

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"
    
class Funcionarios(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    cargo = models.CharField(max_length=50)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    data_admissao = models.DateField()
    data_demissao = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')])

class Folha_Pagamento(models.Model):
    funcionario = models.ForeignKey(Funcionarios, on_delete=models.CASCADE)
    mes_referencia = models.DateField()
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    descontos = models.DecimalField(max_digits=10, decimal_places=2)
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField()

class MetricasFinanceiras(models.Model):
    saldo_caixa = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saldo_caixa_variacao = models.DecimalField(max_digits=5, decimal_places=2)
    
    valor_a_receber = models.DecimalField(max_digits=12, decimal_places=2)
    valor_a_receber_variacao = models.DecimalField(max_digits=5, decimal_places=2)
    
    valor_a_pagar = models.DecimalField(max_digits=12, decimal_places=2)
    valor_a_pagar_variacao = models.DecimalField(max_digits=5, decimal_places=2)
    
    lucro_mensal = models.DecimalField(max_digits=12, decimal_places=2)
    lucro_mensal_variacao = models.DecimalField(max_digits=5, decimal_places=2)
    
    valor_em_estoque = models.DecimalField(max_digits=12, decimal_places=2)
    valor_total_vendas = models.DecimalField(max_digits=12, decimal_places=2)
    
    qtd_fornecedores = models.IntegerField()

    class Meta:
        verbose_name_plural = "Métricas Financeiras"
    @classmethod
    def obter_metricas(cls):
        return cls.objects.first() or cls.objects.create()

class Transacao(models.Model):
    TIPO_CHOICES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('recebido', 'Recebido'),
        ('atrasado', 'Atrasado'),
    ]
    
    data = models.DateField()
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pendente')
    vencimento = models.DateField(null=True, blank=True)
    contraparte = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['-data']
        verbose_name_plural = "Transações"