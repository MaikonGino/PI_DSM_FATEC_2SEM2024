import requests
import random

def buscar_detalhes_receita(receita_id):
    url_detalhes = f"https://api.spoonacular.com/recipes/{receita_id}/information"
    params = {"apiKey": "e5a75baaede34a4c8b869e6325b45472"}
    response_detalhes = requests.get(url_detalhes, params=params)
    response_detalhes.raise_for_status()
    return response_detalhes.json()

def buscar_receita_por_ingredientes(ingredientes_em_ingles):
    # Converte lista de ingredientes em uma string com vírgulas
    ingredientes_str = ','.join(ingredientes_em_ingles)
    print(f"Consulta ingredientes para API: {ingredientes_str}")  # Debug

    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "apiKey": "e5a75baaede34a4c8b869e6325b45472",
        "ingredients": ingredientes_str,
        "number": 20,  # Aumenta o número de receitas retornadas
        "ranking": random.choice([1, 2]),  # Aleatoriza o valor de ranking entre 1 e 2
        "ignorePantry": True
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        receitas = response.json()

        print(f"Receitas encontradas: {receitas}")  # Log completo das receitas encontradas

        # Verificar se as receitas retornaram e contêm os ingredientes
        if not receitas:
            return None

        # Embaralha as receitas para escolher aleatoriamente
        random.shuffle(receitas)

        # Processa os ingredientes de cada receita e inclui quantidade e unidade
        receitas_processadas = []
        for receita in receitas:
            ingredientes_processados = []
            for ingrediente in receita.get('missedIngredients', []):  # A lista de ingredientes ausentes
                nome_ingrediente = ingrediente.get('name', '')
                quantidade = ingrediente.get('amount', 0)
                unidade = ingrediente.get('unit', '')
                
                # Se nome, quantidade ou unidade estiverem ausentes, usa valores padrão
                ingrediente_formatado = {
                    'name': nome_ingrediente,
                    'amount': quantidade,
                    'unit': unidade
                }
                ingredientes_processados.append(ingrediente_formatado)
            
            # Adiciona os ingredientes processados à receita
            receita['ingredientes'] = ingredientes_processados

        # Seleciona a primeira receita após embaralhar
        receita_escolhida = receitas[0] if receitas else None
        return receita_escolhida

    except Exception as e:
        print(f"Erro ao buscar a receita: {e}")
        return None