from fractions import Fraction

from core.utils.traducao import traduzir_unidades, traduzir_ingredientes


def formatar_quantidade(quantidade):
    if quantidade == int(quantidade): 
        return str(int(quantidade))
    else:
        frac = Fraction(quantidade).limit_denominator(10)  
        return str(frac)

def formatar_ingredientes(ingredientes_lista):
    ingredientes_traduzidos = []
    cache_traducao = {}

    for ingrediente in ingredientes_lista:
        nome_ingrediente = ingrediente.get('name', 'Ingrediente desconhecido')
        quantidade = ingrediente.get('amount', 0)
        unidade = ingrediente.get('unit', '').strip()

        nome_traduzido = traduzir_ingredientes([nome_ingrediente], cache_traducao)[0]

        unidade_traduzida = traduzir_unidades(unidade) if unidade else ''  

        quantidade_str = formatar_quantidade(quantidade)

        descricao_traduzida = f"{quantidade_str} {unidade_traduzida} {nome_traduzido}".strip()
        ingredientes_traduzidos.append(descricao_traduzida)

    return ingredientes_traduzidos