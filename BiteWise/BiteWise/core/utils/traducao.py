from core.backends.translator import traduzir_texto_azure
import langdetect



def detectar_idioma(texto):
    try:
        return langdetect.detect(texto)
    except:
        return None

def traduzir_unidades(unidades, dicionario_cache):
    unidades_traduzidas = []
    
    for unidade in unidades:
        if unidade.lower() not in dicionario_cache:
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

        try:
            nome_traduzido = traduzir_texto_azure(ingrediente_limpado, de='en', para='pt')
            
            if nome_traduzido:
                cache_traducao[ingrediente_limpado] = nome_traduzido
                ingredientes_traduzidos.append(nome_traduzido)
            else:
                ingredientes_traduzidos.append(ingrediente_limpado)
        except Exception as e:
            ingredientes_traduzidos.append(ingrediente_limpado)

    return ingredientes_traduzidos

def traduzir_ingredientes_para_busca(ingredientes, cache_traducao):
    ingredientes_traduzidos = []

    for ingrediente in ingredientes:
        ingrediente_limpado = ingrediente.strip()

        if ingrediente_limpado in cache_traducao:
            ingredientes_traduzidos.append(cache_traducao[ingrediente_limpado])
            continue

        try:
            nome_traduzido = traduzir_texto_azure(ingrediente_limpado, de='pt', para='en')
            if nome_traduzido:
                cache_traducao[ingrediente_limpado] = nome_traduzido
                ingredientes_traduzidos.append(nome_traduzido)
            else:
                ingredientes_traduzidos.append(ingrediente_limpado)
        except Exception as e:
            ingredientes_traduzidos.append(ingrediente_limpado)

    return ingredientes_traduzidos

def traduzir_ingredientes_para_exibicao(ingredientes, cache_traducao):
    ingredientes_traduzidos = []

    for ingrediente in ingredientes:
        ingrediente_limpado = ingrediente.strip()

        if ingrediente_limpado in cache_traducao:
            ingredientes_traduzidos.append(cache_traducao[ingrediente_limpado])
            continue

        try:
            nome_traduzido = traduzir_texto_azure(ingrediente_limpado, de='en', para='pt')
            if nome_traduzido:
                cache_traducao[ingrediente_limpado] = nome_traduzido
                ingredientes_traduzidos.append(nome_traduzido)
            else:
                ingredientes_traduzidos.append(ingrediente_limpado)
        except Exception as e:
            ingredientes_traduzidos.append(ingrediente_limpado)

    return ingredientes_traduzidos
