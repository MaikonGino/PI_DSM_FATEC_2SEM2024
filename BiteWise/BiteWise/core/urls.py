from django.urls import path
from . import views


urlpatterns = [
    path('cadastro', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('', views.home, name='home'),
    path('logado', views.homeSignedin, name='home_logged'),
    path('sobre', views.aboutUs, name='about'),
    path('contato', views.contact, name='contato'),
    path('ingredientes/', views.listar_ingredientes, name='listar_ingredientes'),
    path('ingrediente/<str:nome>/', views.detalhes_ingrediente, name='detalhes_ingrediente'),
    
]
