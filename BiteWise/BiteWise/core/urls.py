from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('sobre', views.aboutUs, name='about'),
    path('contato', views.contact, name='contato'),
    path('ingredientes/', views.listar_ingredientes, name='listar_ingredientes'),
    path('ingrediente/<str:nome>/', views.detalhes_ingrediente, name='detalhes_ingrediente'),
    path('Perfil', views.profile, name='perfil'),
    path('buscar_receita/', views.buscar_receita, name='buscar_receita'),
    # auth urls
    path('login/', views.user_login, name='login'),
    path('cadastro/', views.register, name='register'),
    path('accounts/', include('allauth.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
