import requests

def traduzir_texto_azure(texto, de='pt', para='en'):
    chave_api = '6aYIHyO1R0dc6lSfwoFlplrvt6IuvKwWczMHgHdemRGz7SbCRWjeJQQJ99AKACZoyfiXJ3w3AAAbACOGY9BH'
    endpoint = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    parametros = f'&from={de}&to={para}'
    url = endpoint + path + parametros
    
    headers = {
        'Ocp-Apim-Subscription-Key': chave_api,
        'Content-type': 'application/json',
        'Ocp-Apim-Subscription-Region': 'brazilsouth'
    }

    body = [{'text': texto}]
    
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        
        resultados = response.json()
        
        traduzido = resultados[0]['translations'][0]['text']
        
        if traduzido.lower() == texto.lower():
            return texto  
        else:
            return traduzido
    except requests.exceptions.RequestException as e:
        return None