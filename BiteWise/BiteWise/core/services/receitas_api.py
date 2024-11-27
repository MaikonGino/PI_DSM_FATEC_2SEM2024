import requests
import random

def buscar_detalhes_receita(receita_id):
    url_detalhes = f"https://api.spoonacular.com/recipes/{receita_id}/information"
    params = {"apiKey": "e5a75baaede34a4c8b869e6325b45472"}
    response_detalhes = requests.get(url_detalhes, params=params)
    response_detalhes.raise_for_status()
    return response_detalhes.json()

def buscar_receita_por_ingredientes(ingredientes_em_ingles):
    ingredientes_str = ','.join(ingredientes_em_ingles)
    print(f"Consulta ingredientes para API: {ingredientes_str}") 

    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "apiKey": "e5a75baaede34a4c8b869e6325b45472",
        "ingredients": ingredientes_str,
        "number": 5,  
        "ranking": random.choice([1, 2]),  
        "ignorePantry": True
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        receitas = response.json()
        
        if not receitas:
            return None

        random.shuffle(receitas)

        receitas_processadas = []
        for receita in receitas:
            ingredientes_processados = []
            for ingrediente in receita.get('missedIngredients', []):  
                nome_ingrediente = ingrediente.get('name', '')
                quantidade = ingrediente.get('amount', 0)
                unidade = ingrediente.get('unit', '')
                
                ingrediente_formatado = {
                    'name': nome_ingrediente,
                    'amount': quantidade,
                    'unit': unidade
                }
                ingredientes_processados.append(ingrediente_formatado)
            
            receita['ingredientes'] = ingredientes_processados

        receita_escolhida = receitas[0] if receitas else None
        return receita_escolhida

    except Exception as e:
        print(f"Erro ao buscar a receita: {e}")
        return None