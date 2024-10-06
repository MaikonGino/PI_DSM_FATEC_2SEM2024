import requests
from django.shortcuts import render

def buscar_receitas(request):
    if request.method == "POST":
        ingredients_input = request.POST.get("ingredientes")
        
        # Divide os ingredientes em uma lista e remove espaços extras
        ingredients = [ingredient.strip().lower() for ingredient in ingredients_input.split(',')]
        
        #adicionar APIS
        api_urls = {
            'receitas': 'https://api-receitas-pi.vercel.app/receitas/todas',
            'outra_api': 'https://api.spoonacular.com/recipes/complexSearch'
        }
        
        receitas_data = []
        outra_api_data = []

  
        try:
            response_receitas = requests.get(api_urls['receitas'])
            if response_receitas.status_code == 200:
                receitas_data = response_receitas.json()
            else:
                return render(request, 'erro.html', {'mensagem': f'Erro na API de receitas: {response_receitas.status_code}'})
        
        except requests.exceptions.RequestException as e:
            return render(request, 'erro.html', {'mensagem': f'Erro na requisição da API de receitas: {e}'})

       #repetir verificação se houver mais
        try:
            response_outra_api = requests.get(api_urls['outra_api'])
            if response_outra_api.status_code == 200:
                outra_api_data = response_outra_api.json()
            else:
                return render(request, 'erro.html', {'mensagem': f'Erro na Outra API: {response_outra_api.status_code}'})
        
        except requests.exceptions.RequestException as e:
            return render(request, 'erro.html', {'mensagem': f'Erro na requisição da Outra API: {e}'})

        # Filtro de receitas com os dados que o usuario digitou
        matching_recipes = []
        for recipe in receitas_data:
            recipe_ingredients = [ingredient.lower() for ingredient in recipe.get('ingredientes', [])]
            if any(ingredient in recipe_ingredients for ingredient in ingredients):
                matching_recipes.append(recipe)

        # Processar dados da outra API, se necessário (depende da estrutura da resposta)
        # Exemplo: matching_outros_dados = alguma_filtro(outra_api_data)

        return render(request, 'resultados.html', {
            'receitas': matching_recipes,
            'dados_outra_api': outra_api_data,  # Adiciona dados da segunda API
            'ingredientes': ingredients
        })
    
    return render(request, 'busca.html')
