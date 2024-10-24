from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

urlpatterns = [
    path('cadastro', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('sobre', views.aboutUs, name='about'),
    path('contato', views.contact, name='contato'),
    path('ingredientes/', views.listar_ingredientes, name='listar_ingredientes'),
    path('ingrediente/<str:nome>/', views.detalhes_ingrediente, name='detalhes_ingrediente'),
    path('Perfil', views.profile, name='perfil'),
    
    # auth urls
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
