from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from core.utils.traducao import traduzir_ingredientes_para_busca, traduzir_ingredientes_para_exibicao, traduzir_unidades
from core.services.receitas_api import buscar_detalhes_receita, buscar_receita_por_ingredientes
from .models import Ingrediente 
from django.contrib.auth.views import LoginView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from .backends.translator import traduzir_texto_azure
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model




# Create your views here.
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
    user = request.user  # Obter o usuário logado
    
    context = {
        'user': user,
        # Não há necessidade de buscar um modelo separado para o Google.
        # Agora os dados do Google estão diretamente no modelo CustomUser.
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
    # Verifica se o usuário já está autenticado
    if request.user.is_authenticated:
        return redirect('home')  # Redireciona para a home se o usuário já estiver logado

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentica o usuário
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Realiza o login
            return redirect('home')  # Redireciona para a home após login bem-sucedido
        else:
            messages.error(request, "Usuário ou senha inválidos.")  # Exibe erro caso o login falhe

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

def buscar_receita(request):
    # Extrai os ingredientes do request, dividindo por vírgulas e espaços
    ingredientes = request.GET.get('ingredientes')
    if not ingredientes:
        return exibir_erro(request, 'Nenhum ingrediente fornecido.')

    # Divide os ingredientes em uma lista de palavras, separando por vírgula
    ingredientes_lista = [ingrediente.strip() for ingrediente in ingredientes.split(',') if ingrediente.strip()]

    # Traduza os ingredientes para inglês para a busca
    ingredientes_em_ingles = traduzir_ingredientes_para_busca(ingredientes_lista, {})
    print(f"Ingredientes traduzidos para inglês para busca: {ingredientes_em_ingles}")

    if not ingredientes_em_ingles:
        return exibir_erro(request, 'Erro ao traduzir os ingredientes fornecidos para a busca.')

    # Busca a receita por ingredientes
    receita = buscar_receita_por_ingredientes(ingredientes_em_ingles)
    if not receita:
        return exibir_erro(request, 'Nenhuma receita encontrada com os ingredientes fornecidos.')

    try:
        nome_traduzido, instrucoes_traduzidas, ingredientes_lista, imagem = obter_detalhes_traduzidos(receita['id'])
        
        # Certifique-se de que ingredientes_lista seja uma lista de dicionários com 'name', 'amount' e 'unit'
        ingredientes_com_quantidade = []
        dicionario_unidades = {}  # Cache para as unidades

        for ingrediente_original in receita['ingredientes']:
            nome_ingrediente = ingrediente_original.get('name', '')
            quantidade = ingrediente_original.get('amount', 0)
            unidade = ingrediente_original.get('unit', '')

            # Traduz o nome do ingrediente para português
            nome_ingrediente_traduzido = traduzir_ingredientes_para_exibicao([nome_ingrediente], {})[0]

            # Traduz a unidade de medida, se houver
            unidades_traduzidas = traduzir_unidades([unidade], dicionario_unidades)

            # Corrigir a quantidade para remover casas decimais desnecessárias
            if quantidade.is_integer():
                quantidade_formatada = str(int(quantidade))  # Se for inteiro, mostra sem casas decimais
            else:
                quantidade_formatada = str(quantidade)  # Caso contrário, mantém o número com casas decimais

            # Formatar o ingrediente com quantidade, unidade e nome traduzido
            ingrediente_completo = f"{quantidade_formatada} {unidades_traduzidas[0]} de {nome_ingrediente_traduzido}".strip()
            ingredientes_com_quantidade.append(ingrediente_completo)

    except Exception as e:
        print(f"Erro ao obter detalhes da receita: {e}")
        return exibir_erro(request, 'Erro ao buscar a receita. Tente novamente mais tarde.')

    context = {
        'nome': nome_traduzido,
        'imagem': imagem,
        'ingredientes': ingredientes_com_quantidade,  # Ingredientes formatados com quantidade e unidade
        'instrucoes': instrucoes_traduzidas,
    }
    return render(request, 'resultado_receita.html', context)

def register(request):
    # Verifica se o usuário já está autenticado
    if request.user.is_authenticated:
        return redirect('home')  # Redireciona para a home (ou outra página desejada) se o usuário já estiver logado

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Criação do usuário
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash da senha
            user.save()  # Salva no banco de dados
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('login')  # Redireciona para a página de login ou outra
        else:
            # Verifica os erros do formulário
            for field, errors in form.errors.items():
                print(f"Erro no campo {field}: {errors}")  # Imprime os erros
            messages.error(request, 'Erro ao cadastrar usuário. Verifique os dados.')
            # Não redireciona, apenas re-renderiza a página com os erros
    else:
        # Se for uma requisição GET, cria um formulário vazio
        form = UserRegistrationForm()

    return render(request, 'signup.html', {'form': form})

