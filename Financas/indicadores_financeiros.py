
from Financas.utils import total_despesas, total_vendas

def lucro_liquido():
    """
    Calcula o lucro líquido de uma empresa.
    O lucro líquido é calculado como (Total de Vendas - Total de Despesas).
    """
    try: 
        lucro = total_vendas() - total_despesas()
        if lucro is None:
            raise ValueError("O lucro líquido não pode ser nulo.") 
        return lucro
    except ValueError as e:
        print(f"Erro: {e}")
        return None

def margem_lucro():
    """
    Calcula a margem de lucro de uma empresa.
    A margem de lucro é calculada como (Lucro Líquido / Receita Líquida) * 100.
    """
    try: 
        lucro_liquido = lucro_liquido() # Chama a função lucro_liquido para obter o lucro líquido
        if lucro_liquido is None:
            raise ValueError("O lucro líquido não pode ser nulo.") 
        
        receita_liquida = total_vendas()
        if receita_liquida == 0:
            raise ValueError("A receita líquida não pode ser zero.")
        margem = (lucro_liquido / receita_liquida) * 100
        return margem
    except ValueError as e:
        print(f"Erro: {e}")
        return None