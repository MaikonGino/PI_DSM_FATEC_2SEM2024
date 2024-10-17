from django.urls import path
from . import views

urlpatterns = [
    path('cadastro', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('', views.home, name='home'),
    path('logado', views.homeSignedin, name='home_logged'),
    path('sobre', views.aboutUs, name='about')
]