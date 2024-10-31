from django.urls import path
from . import views
from .views import CustomLoginView


urlpatterns = [
    path('cadastro', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]