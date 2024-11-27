import json
from django.http import JsonResponse
from django.utils.timezone import now
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from core.utils.formatacao import formatar_quantidade
from core.backends.calculation import calcular_dificuldade
from core.utils.traducao import traduzir_ingredientes_para_busca, traduzir_ingredientes_para_exibicao, traduzir_unidades
from core.services.receitas_api import buscar_detalhes_receita, buscar_receita_por_ingredientes
from .models import Ingrediente, IngredienteReceita, Receita 
from django.views.decorators.cache import never_cache
from .backends.translator import traduzir_texto_azure
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def signup (request):
    return render(request, 'signup.html')

@never_cache
def home (request):
    return render(request, 'home.html')

def aboutUs (request):
    return render (request, 'aboutUs.html')

def contact (request):
    return render (request, 'contact.html')

@login_required
def profile(request):
    user = request.user  
    
    context = {
        'user': user,
        'google_profile': {
            'google_id': user.google_id,
            'profile_picture': user.profile_picture
        } if user.google_id else None,
    }
    return render(request, 'profile.html', context)

def listar_ingredientes (request):
    ingredientes = Ingrediente.objects.all()
    return render(request, 'listar_ingredientes.html', {'ingredientes': ingredientes})

def detalhes_ingrediente (request, nome):
    ingrediente = get_object_or_404(Ingrediente, nome=nome)
    return render(request, 'detalhes_ingrediente.html', {'ingrediente': ingrediente})

@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home') 

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user) 
            return redirect('home')  
        else:
            messages.error(request, "Usuário ou senha inválidos.")  

    return render(request, 'login.html')

def exibir_erro(request, mensagem):
    return render(request, 'erro.html', {'mensagem': mensagem})

def obter_detalhes_traduzidos(receita_id):
    receita_detalhes = buscar_detalhes_receita(receita_id)
    try:
        nome_traduzido = traduzir_texto_azure(receita_detalhes.get('title', 'Receita Sem Título'), de='en', para='pt')
        instrucoes_traduzidas = traduzir_texto_azure(receita_detalhes.get('instructions', 'Sem instruções disponíveis.'), de='en', para='pt')
    except Exception as e:
        print(f"Erro ao traduzir o título ou instruções: {e}")
        nome_traduzido = receita_detalhes.get('title', 'Receita Sem Título')
        instrucoes_traduzidas = receita_detalhes.get('instructions', 'Sem instruções disponíveis.')
    return nome_traduzido, instrucoes_traduzidas, receita_detalhes.get('extendedIngredients', []), receita_detalhes.get('image', '')



def traduzir_texto_longo(texto, de='auto', para='pt'):
    """Divide um texto longo em partes para tradução e concatena os resultados."""
    partes = [texto[i:i+5000] for i in range(0, len(texto), 5000)]  
    texto_traduzido = ''
    for parte in partes:
        texto_traduzido += traduzir_texto_azure(parte, de, para) + ' '
    return texto_traduzido.strip()

def salvar_receita_no_banco(
    detalhes_receita, 
    nome_traduzido, 
    instrucoes_traduzidas, 
    dicas_traduzidas, 
    ingredientes_com_quantidade
):
    """
    Salva os detalhes de uma receita no banco de dados.
    Se a receita já existir, apenas atualiza os campos modificados.
    """
    receita, criada = Receita.objects.get_or_create(
        id_receita=detalhes_receita['id'], 
        defaults={
            'titulo': detalhes_receita.get('title', 'Receita Sem Título'),
            'titulo_traduzido': nome_traduzido,
            'imagem': detalhes_receita.get('image', ''),
            'tempo_preparo': detalhes_receita.get('preparationMinutes'),
            'tempo_total': detalhes_receita.get('readyInMinutes'),
            'porcoes': detalhes_receita.get('servings'),
            'dicas': detalhes_receita.get('summary', 'Dicas não disponíveis.'),
            'dicas_traduzidas': dicas_traduzidas,
            'instrucoes': detalhes_receita.get('instructions', 'Instruções não disponíveis.'),
            'instrucoes_traduzidas': instrucoes_traduzidas,
        }
    )

    if not criada:
        receita.titulo_traduzido = nome_traduzido
        receita.dicas_traduzidas = dicas_traduzidas
        receita.instrucoes_traduzidas = instrucoes_traduzidas
        receita.ultima_atualizacao = now()
        receita.save()

    ingredientes_existentes = set(
        IngredienteReceita.objects.filter(receita=receita).values_list('nome', flat=True)
    )

    for ingrediente_original in detalhes_receita.get('extendedIngredients', []):
        nome_ingrediente = ingrediente_original.get('name', '')

        if nome_ingrediente not in ingredientes_existentes:
            IngredienteReceita.objects.create(
                receita=receita,
                nome=nome_ingrediente,
                nome_traduzido=ingredientes_com_quantidade.get(nome_ingrediente, nome_ingrediente),
                quantidade=ingrediente_original.get('amount', 0),
                unidade=ingrediente_original.get('unit', ''),
                unidade_traduzida=ingredientes_com_quantidade.get(
                    ingrediente_original.get('unit', ''), 
                    ingrediente_original.get('unit', '')
                ),
            )   

def buscar_receita(request):
    """Busca receitas por ingredientes fornecidos pelo usuário, traduz e salva os detalhes no banco."""
    ingredientes = request.GET.get('ingredientes')
    if not ingredientes:
        return exibir_erro(request, 'Nenhum ingrediente fornecido.')

    ingredientes_lista = [ingrediente.strip() for ingrediente in ingredientes.split(',') if ingrediente.strip()]

    try:
        ingredientes_em_ingles = traduzir_ingredientes_para_busca(ingredientes_lista, {})
    except Exception as e:
        print(f"Erro ao traduzir os ingredientes: {e}")
        return exibir_erro(request, 'Erro ao traduzir os ingredientes fornecidos para a busca.')

    if not ingredientes_em_ingles:
        return exibir_erro(request, 'Erro ao processar os ingredientes fornecidos.')

    receita = buscar_receita_por_ingredientes(ingredientes_em_ingles)
    if not receita:
        return exibir_erro(request, 'Nenhuma receita encontrada com os ingredientes fornecidos.')

    try:
        detalhes_receita = buscar_detalhes_receita(receita['id'])
        instrucoes = detalhes_receita.get('instructions', 'Instruções não disponíveis.')
        dicas = detalhes_receita.get('summary', 'Dicas não disponíveis.')
        instrucoes_traduzidas = traduzir_texto_longo(instrucoes, de='en', para='pt')
        dicas_traduzidas = traduzir_texto_longo(dicas, de='en', para='pt')

        tempo_preparo = detalhes_receita.get('preparationMinutes', 'Indisponível')
        tempo_total = detalhes_receita.get('readyInMinutes', 'Indisponível')
        porcoes = detalhes_receita.get('servings', 'Indisponível')
        imagem = detalhes_receita.get('image', '')

        ingredientes_com_quantidade = {}
        for ingrediente_original in detalhes_receita.get('extendedIngredients', []):
            nome_ingrediente = ingrediente_original.get('name', '')
            quantidade = ingrediente_original.get('amount', 0)
            unidade = ingrediente_original.get('unit', '')

            quantidade_formatada = formatar_quantidade(quantidade)

            nome_ingrediente_traduzido = traduzir_ingredientes_para_exibicao([nome_ingrediente], {})[0]
            unidade_traduzida = traduzir_unidades([unidade], {})[0]

            ingredientes_com_quantidade[nome_ingrediente] = {
                'nome_traduzido': nome_ingrediente_traduzido,
                'quantidade': quantidade_formatada,
                'unidade': unidade,
                'unidade_traduzida': unidade_traduzida
            }
    
        salvar_receita_no_banco(
            detalhes_receita,
            nome_traduzido=detalhes_receita.get('title', 'Receita Sem Título'),
            instrucoes_traduzidas=instrucoes_traduzidas,
            dicas_traduzidas=dicas_traduzidas,
            ingredientes_com_quantidade=ingredientes_com_quantidade
        )

        ingredientes_formatados = [
            f"{dados['quantidade']} {dados['unidade_traduzida']} de {dados['nome_traduzido']}".strip()
            for dados in ingredientes_com_quantidade.values()
        ]

    except Exception as e:
        print(f"Erro ao obter detalhes da receita: {e}")
        return exibir_erro(request, 'Erro ao buscar a receita. Tente novamente mais tarde.')

    context = {
        'nome': detalhes_receita.get('title', 'Receita Sem Título'),
        'imagem': imagem,
        'ingredientes': ingredientes_formatados,
        'instrucoes': instrucoes_traduzidas,
        'tempo_preparo': tempo_preparo,
        'tempo_total': tempo_total,
        'porcoes': porcoes,
        'dificuldade': calcular_dificuldade(tempo_total),
        'dicas': dicas_traduzidas,
        'armazenamento': 'Armazene em local fresco por até 3 dias.',  
    }
    return render(request, 'recipe_search.html', context)




def register(request):
    if request.user.is_authenticated:
        return redirect('home')  

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            user.save()  
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('login')  
        else:
            for field, errors in form.errors.items():
                print(f"Erro no campo {field}: {errors}")  
            messages.error(request, 'Erro ao cadastrar usuário. Verifique os dados.')
    else:
        form = UserRegistrationForm()

    return render(request, 'signup.html', {'form': form})


def api_send_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            opcao = data.get('options')
            mensagem = data.get('message')
            nome = data.get('name')
            email = data.get('email')  
            telefone = data.get('phone')

            assunto = f"Novo Contato de {nome} - {opcao}"

            mensagem_email = (
                f"Nome: {nome}\n"
                f"E-mail: {email}\n"
                f"Telefone: {telefone}\n\n"
                f"Mensagem:\n{mensagem}"
            )

            destinatario = 'bitewise.contato@gmail.com'

            send_mail(
                assunto,  
                mensagem_email,  
                email,  
                [destinatario],  
                fail_silently=False,  
            )

            return JsonResponse({'message': 'E-mail enviado com sucesso!'}, status=200)

        except Exception as e:
            return JsonResponse({'message': f'Erro ao enviar o e-mail: {e}'}, status=500)

    return JsonResponse({'message': 'Método não permitido'}, status=405)