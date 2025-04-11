import datetime
from Financas.controller import get_folha_pagamento, get_imposto, get_vendas, set_fluxo_caixa
from Financas.models import Fluxo_Caixa, Venda




def total_vendas():
    """
    Função para obter o total de vendas.
    """
    try:
        total = get_vendas.values('valor_total').aggregate(sum('valor_total'))
        return total
    except Venda.DoesNotExist:
        return None
    
def total_despesas():
    """
    Função para obter o total de despesas.
    """
    try:
        total = get_imposto.objects.aggregate(sum('valor')) + get_folha_pagamento.objects.aggregate(sum('salario_base'))
        return total
    except get_folha_pagamento.DoesNotExist:
        return None

def fluxo_caixa():    
    """
    Função para obter o fluxo de caixa.
    """
    try:
        total_vendas = total_vendas()
        if total_vendas is None:
            return None
        
        total_despesas = total_despesas()
        if total_despesas is None:
            return None
        
        saldo = total_vendas - total_despesas

        data = datetime.now().month().year()

        descricao = 'Fluxo de Caixa'

        set_fluxo_caixa(
            data=data,
            defaults={
                'descricao': descricao,
                'total_vendas': total_vendas,
                'total_despesas': total_despesas,
                'saldo_acumulado': saldo
            }
        )
        return set_fluxo_caixa(fluxo_caixa)
    except Fluxo_Caixa.DoesNotExist:
        return None
    

def faturamento():
    """
    Função para obter o faturamento.
    """
    try:
        quantidade_vendas = [sum(vendas) for vendas in get_vendas.values('pago')]
        total = total_vendas() * quantidade_vendas
        return total
    except Venda.DoesNotExist:
        return None
    
