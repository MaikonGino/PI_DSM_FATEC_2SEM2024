from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Ingrediente

# Create your views here.
def signup (request):
    return render(request, 'signup.html')
    
def login (request):
    return render(request, 'login.html')

def home (request):
    return render(request, 'home.html')

def homeSignedin (request):
    return render (request, 'home_logged.html')

def aboutUs (request):
    return render (request, 'aboutUs.html')

def contact (request):
    return render (request, 'contact.html')

def listar_ingredientes (request):
    ingredientes = Ingrediente.objects.all()
    return render(request, 'listar_ingredientes.html', {'ingredientes': ingredientes})

def detalhes_ingrediente (request, nome):
    ingrediente = get_object_or_404(Ingrediente, nome=nome)
    return render(request, 'detalhes_ingrediente.html', {'ingrediente': ingrediente})