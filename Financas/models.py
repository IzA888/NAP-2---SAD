from django.db import models

# Create your models here.
class Produto(models.Model):
    codigo = models.CharField(max_length=20, unique=True),
    descricao = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50)
    data_cadastro = models.DateField(auto_now_add=True)

class Fluxo_Caixa(models.Model):
    data = models.DateField()
    descricao = models.CharField(max_length=100)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('saida', 'Saída')])
    saldo_acumulado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

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

class Produto_Estoque(models.Model):
    codigo_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade_disponivel = models.IntegerField()
    data_entrada = models.DateField()
    data_saida = models.DateField(null=True, blank=True)

class Vendas(models.Model):
    numero_pedido = models.CharField(max_length=20, unique=True)
    data = models.DateField()
    cliente = models.CharField(max_length=100)
    Produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pago', 'Pago'), ('pendente', 'Pendente')])

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

