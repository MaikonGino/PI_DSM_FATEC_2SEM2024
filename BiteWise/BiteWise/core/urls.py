from django.urls import path
from . import views

urlpatterns = [
    path('cadastro', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('', views.home, name='home')
]