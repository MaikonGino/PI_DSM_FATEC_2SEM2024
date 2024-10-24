from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Ingrediente
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

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

def profile (request):
    return render (request, 'profile.html')

def listar_ingredientes (request):
    ingredientes = Ingrediente.objects.all()
    return render(request, 'listar_ingredientes.html', {'ingredientes': ingredientes})

def detalhes_ingrediente (request, nome):
    ingrediente = get_object_or_404(Ingrediente, nome=nome)
    return render(request, 'detalhes_ingrediente.html', {'ingrediente': ingrediente})

def login (request):
    return render(request, 'login.html')

class CustomLoginView(LoginView):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # If user is already authenticated, redirects user to the logged home
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)