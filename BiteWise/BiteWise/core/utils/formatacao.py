from fractions import Fraction

from core.utils.traducao import traduzir_unidades, traduzir_ingredientes


def formatar_quantidade(quantidade):
    if quantidade.is_integer():
        return str(int(quantidade))
    return str(Fraction(quantidade).limit_denominator(8))

def formatar_ingredientes(ingredientes_lista):
    ingredientes_traduzidos = []
    cache_traducao = {}

    for ingrediente in ingredientes_lista:
        nome_ingrediente = ingrediente.get('name', 'Ingrediente desconhecido')
        quantidade = ingrediente.get('amount', 0)
        unidade = ingrediente.get('unit', '').strip()

        # Traduzir apenas o nome do ingrediente
        nome_traduzido = traduzir_ingredientes([nome_ingrediente], cache_traducao)[0]

        # Traduzir unidade apenas se for necessário
        unidade_traduzida = traduzir_unidades(unidade) if unidade else ''  # Traduza a unidade, se houver

        # Formatar a quantidade
        quantidade_str = formatar_quantidade(quantidade)

        # Montar a descrição traduzida
        descricao_traduzida = f"{quantidade_str} {unidade_traduzida} {nome_traduzido}".strip()
        ingredientes_traduzidos.append(descricao_traduzida)

    return ingredientes_traduzidos