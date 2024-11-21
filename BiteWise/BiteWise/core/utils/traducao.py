from core.backends.translator import traduzir_texto_azure
import langdetect

def detectar_idioma(texto):
    try:
        return langdetect.detect(texto)
    except:
        return None

def traduzir_unidades(unidades, dicionario_cache):
    # Função para traduzir unidades de medida
    unidades_traduzidas = []
    
    for unidade in unidades:
        if unidade.lower() not in dicionario_cache:
            # Faz a tradução da unidade
            resposta = traduzir_texto_azure(unidade, 'en', 'pt')
            if resposta:
                dicionario_cache[unidade.lower()] = resposta
            else:
                dicionario_cache[unidade.lower()] = unidade

        unidades_traduzidas.append(dicionario_cache[unidade.lower()])
    
    return unidades_traduzidas

def traduzir_ingredientes(ingredientes, cache_traducao):
    ingredientes_traduzidos = []

    for ingrediente in ingredientes:
        ingrediente_limpado = ingrediente.strip()

        # Forçar tradução de todos os ingredientes para o português, mesmo que estejam em inglês
        try:
            # Detecta o idioma do ingrediente
            idioma_detectado = detectar_idioma(ingrediente_limpado)
            if idioma_detectado == 'en':
                print(f"Ingrediente '{ingrediente_limpado}' detectado como inglês. Traduzindo para português.")

            # Traduzir o ingrediente do inglês para o português
            nome_traduzido = traduzir_texto_azure(ingrediente_limpado, de='en', para='pt')
            if nome_traduzido:
                print(f"Tradução do ingrediente '{ingrediente_limpado}': '{nome_traduzido}'")
                cache_traducao[ingrediente_limpado] = nome_traduzido
                ingredientes_traduzidos.append(nome_traduzido)
            else:
                # Caso a tradução não ocorra corretamente, mantém o ingrediente original
                print(f"Falha ou ausência de tradução para o ingrediente '{ingrediente_limpado}'. Usando original.")
                ingredientes_traduzidos.append(ingrediente_limpado)
        except Exception as e:
            print(f"Erro ao traduzir o ingrediente '{ingrediente_limpado}': {e}")
            ingredientes_traduzidos.append(ingrediente_limpado)

    return ingredientes_traduzidos

def traduzir_ingredientes_para_busca(ingredientes, cache_traducao):
    ingredientes_traduzidos = []

    for ingrediente in ingredientes:
        ingrediente_limpado = ingrediente.strip()

        # Tenta pegar do cache
        if ingrediente_limpado in cache_traducao:
            ingredientes_traduzidos.append(cache_traducao[ingrediente_limpado])
            continue

        try:
            # Traduz de português para inglês
            nome_traduzido = traduzir_texto_azure(ingrediente_limpado, de='pt', para='en')
            if nome_traduzido:
                print(f"Tradução para a busca do ingrediente '{ingrediente_limpado}': '{nome_traduzido}'")
                cache_traducao[ingrediente_limpado] = nome_traduzido
                ingredientes_traduzidos.append(nome_traduzido)
            else:
                # Se a tradução falhar, usa o nome original
                ingredientes_traduzidos.append(ingrediente_limpado)
        except Exception as e:
            print(f"Erro ao traduzir para a busca o ingrediente '{ingrediente_limpado}': {e}")
            ingredientes_traduzidos.append(ingrediente_limpado)

    return ingredientes_traduzidos

def traduzir_ingredientes_para_exibicao(ingredientes, cache_traducao):
    ingredientes_traduzidos = []

    for ingrediente in ingredientes:
        ingrediente_limpado = ingrediente.strip()

        # Tenta pegar do cache
        if ingrediente_limpado in cache_traducao:
            ingredientes_traduzidos.append(cache_traducao[ingrediente_limpado])
            continue

        try:
            # Traduz de inglês para português
            nome_traduzido = traduzir_texto_azure(ingrediente_limpado, de='en', para='pt')
            if nome_traduzido:
                print(f"Tradução para exibição do ingrediente '{ingrediente_limpado}': '{nome_traduzido}'")
                cache_traducao[ingrediente_limpado] = nome_traduzido
                ingredientes_traduzidos.append(nome_traduzido)
            else:
                # Se a tradução falhar, usa o nome original
                ingredientes_traduzidos.append(ingrediente_limpado)
        except Exception as e:
            print(f"Erro ao traduzir para exibição o ingrediente '{ingrediente_limpado}': {e}")
            ingredientes_traduzidos.append(ingrediente_limpado)

    return ingredientes_traduzidos
