from .models import (Fluxo_Caixa, Folha_Pagamento, Funcionarios, Imposto, MetricasFinanceiras, 
                    Nota_Fiscal, Produto, Produto_Estoque, Vendas)


def get_produto(codigo_produto):
    """
    Função para obter um produto pelo código.
    """
    try:
        produto = Produto.objects.get('codigo'==codigo_produto)
        return produto
    except Produto.DoesNotExist:
        return None
    
def set_produto(codigo_produto, descricao, preco, categoria, fornecedor):
    """
    Função para criar ou atualizar um produto.
    """
    produto, created = Produto.objects.update_or_create(
        codigo=codigo_produto,
        defaults={
            'descricao': descricao,
            'preco': preco,
            'categoria': categoria,
            'fornecedor': fornecedor
        }
    )
    return produto

def delete_produto(codigo_produto):
    """
    Função para deletar um produto pelo código.
    """
    try:
        produto = Produto.objects.get(codigo=codigo_produto)
        produto.delete()
        return True
    except Produto.DoesNotExist:
        return False
    
def get_fluxo_caixa(data):
    """
    Função para obter um fluxo de caixa pela data.
    """
    try:
        fluxo_caixa = Fluxo_Caixa.objects.get(data=data)
        return fluxo_caixa
    except Fluxo_Caixa.DoesNotExist:
        return None

def set_fluxo_caixa(data, descricao, produto, valor, tipo):
    """
    Função para criar ou atualizar um fluxo de caixa.
    """
    fluxo_caixa, created = Fluxo_Caixa.objects.update_or_create(
        data=data,
        defaults={
            'descricao': descricao,
            'produto': produto,
            'valor': valor,
            'tipo': tipo
        }
    )
    return fluxo_caixa

def delete_fluxo_caixa(data):
    """
    Função para deletar um fluxo de caixa pela data.
    """
    try:
        fluxo_caixa = Fluxo_Caixa.objects.get(data=data)
        fluxo_caixa.delete()
        return True
    except Fluxo_Caixa.DoesNotExist:
        return False
    
def get_nota_fiscal(numero_nota):
    """
    Função para obter uma nota fiscal pelo número.
    """
    try:
        nota_fiscal = Nota_Fiscal.objects.get(numero=numero_nota)
        return nota_fiscal
    except Nota_Fiscal.DoesNotExist:
        return None 
    
def set_nota_fiscal(numero_nota, data_emissao, valor_total, imposto):
    """
    Função para criar ou atualizar uma nota fiscal.
    """
    nota_fiscal, created = Nota_Fiscal.objects.update_or_create(
        numero=numero_nota,
        defaults={
            'data_emissao': data_emissao,
            'valor_total': valor_total,
            'imposto': imposto
        }
    )
    return nota_fiscal

def delete_nota_fiscal(numero_nota):
    """
    Função para deletar uma nota fiscal pelo número.
    """
    try:
        nota_fiscal = Nota_Fiscal.objects.get(numero=numero_nota)
        nota_fiscal.delete()
        return True
    except Nota_Fiscal.DoesNotExist:
        return False    
    
def get_imposto(tipo_imposto):
    """
    Função para obter um imposto pelo tipo.
    """
    try:
        imposto = Imposto.objects.get(tipo=tipo_imposto)
        return imposto
    except Imposto.DoesNotExist:
        return None
    
def set_imposto(tipo_imposto, valor, data_emissao, status): 
    """
    Função para criar ou atualizar um imposto.
    """
    imposto, created = Imposto.objects.update_or_create(
        tipo=tipo_imposto,
        defaults={
            'valor': valor,
            'data_emissao': data_emissao,
            'status': status
        }
    )
    return imposto 

def delete_imposto(tipo_imposto):
    """
    Função para deletar um imposto pelo tipo.
    """
    try:
        imposto = Imposto.objects.get(tipo=tipo_imposto)
        imposto.delete()
        return True
    except Imposto.DoesNotExist:
        return False
    
def get_produto_estoque(codigo_produto):
    """
    Função para obter um produto em estoque pelo código.
    """
    try:
        produto_estoque = Produto_Estoque.objects.get(codigo_produto=codigo_produto)
        return produto_estoque
    except Produto_Estoque.DoesNotExist:
        return None
    
def set_produto_estoque(codigo_produto, quantidade_disponivel, data_entrada, data_saida):
    """
    Função para criar ou atualizar um produto em estoque.
    """
    produto_estoque, created = Produto_Estoque.objects.update_or_create(
        codigo_produto=codigo_produto,
        defaults={
            'quantidade_disponivel': quantidade_disponivel,
            'data_entrada': data_entrada,
            'data_saida': data_saida
        }
    )
    return produto_estoque

def delete_produto_estoque(codigo_produto):
    """
    Função para deletar um produto em estoque pelo código.
    """
    try:
        produto_estoque = Produto_Estoque.objects.get(codigo_produto=codigo_produto)
        produto_estoque.delete()
        return True
    except Produto_Estoque.DoesNotExist:
        return False

def get_vendas(numero_pedido):
    """
    Função para obter uma venda pelo número do pedido.
    """
    try:
        vendas = Vendas.objects.get(numero_pedido=numero_pedido)
        return vendas
    except Vendas.DoesNotExist:
        return None
    
def set_vendas(numero_pedido, data, cliente, produto, valor_total, status):
    """
    Função para criar ou atualizar uma venda.
    """
    vendas, created = Vendas.objects.update_or_create(
        numero_pedido=numero_pedido,
        defaults={
            'data': data,
            'cliente': cliente,
            'produto': produto,
            'valor_total': valor_total,
            'status': status
        }
    )
    return vendas

def delete_vendas(numero_pedido):
    """
    Função para deletar uma venda pelo número do pedido.
    """
    try:
        vendas = Vendas.objects.get(numero_pedido=numero_pedido)
        vendas.delete()
        return True
    except Vendas.DoesNotExist:
        return False

def get_funcionarios(cpf):
    """
    Função para obter um funcionário pelo CPF.
    """
    try:
        funcionarios = Funcionarios.objects.get(cpf=cpf)
        return funcionarios
    except Funcionarios.DoesNotExist:
        return None

def set_funcionarios(cpf, nome, endereco, telefone, email, cargo, salario, data_admissao, data_demissao, status):
    """
    Função para criar ou atualizar um funcionário.
    """
    funcionarios, created = Funcionarios.objects.update_or_create(
        cpf=cpf,
        defaults={
            'nome': nome,
            'endereco': endereco,
            'telefone': telefone,
            'email': email,
            'cargo': cargo,
            'salario': salario,
            'data_admissao': data_admissao,
            'data_demissao': data_demissao,
            'status': status
        }
    )
    return funcionarios   

def delete_funcionarios(cpf):
    """
    Função para deletar um funcionário pelo CPF.
    """
    try:
        funcionarios = Funcionarios.objects.get(cpf=cpf)
        funcionarios.delete()
        return True
    except Funcionarios.DoesNotExist:
        return False
    
def get_folha_pagamento(mes_referencia):
    """
    Função para obter uma folha de pagamento pelo mês de referência.
    """
    try:
        folha_pagamento = Folha_Pagamento.objects.get(mes_referencia=mes_referencia)
        return folha_pagamento
    except Folha_Pagamento.DoesNotExist:
        return None
    
def set_folha_pagamento(mes_referencia, funcionario, salario_base, descontos, valor_liquido, data_pagamento):
    """
    Função para criar ou atualizar uma folha de pagamento.
    """
    folha_pagamento, created = Folha_Pagamento.objects.update_or_create(
        mes_referencia=mes_referencia,
        defaults={
            'funcionario': funcionario,
            'salario_base': salario_base,
            'descontos': descontos,
            'valor_liquido': valor_liquido,
            'data_pagamento': data_pagamento
        }
    )
    return folha_pagamento
    
def get_metricas_financeiras():
    """
    Função para obter as métricas financeiras.
    """
    try:
        metricas = MetricasFinanceiras.objects.all()
        return metricas
    except MetricasFinanceiras.DoesNotExist:
        return None
    
def set_metricas_financeiras(saldo_caixa, saldo_caixa_variacao, valor_a_receber, valor_a_receber_variacao,
                            valor_a_pagar, valor_a_pagar_variacao, lucro_mensal, lucro_mensal_variacao):
    """
    Função para criar ou atualizar as métricas financeiras.
    """
    metricas_financeiras, created = MetricasFinanceiras.objects.update_or_create(
        saldo_caixa=saldo_caixa,
        defaults={
            'saldo_caixa_variacao': saldo_caixa_variacao,
            'valor_a_receber': valor_a_receber,
            'valor_a_receber_variacao': valor_a_receber_variacao,
            'valor_a_pagar': valor_a_pagar,
            'valor_a_pagar_variacao': valor_a_pagar_variacao,
            'lucro_mensal': lucro_mensal,
            'lucro_mensal_variacao': lucro_mensal_variacao
        }
    )
    return metricas_financeiras


def delete_metricas_financeiras(saldo_caixa):
    """
    Função para deletar as métricas financeiras pelo saldo de caixa.
    """
    try:
        metricas_financeiras = MetricasFinanceiras.objects.get(saldo_caixa=saldo_caixa)
        metricas_financeiras.delete()
        return True
    except MetricasFinanceiras.DoesNotExist:
        return False
    