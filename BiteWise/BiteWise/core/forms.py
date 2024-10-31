# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class CustomLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        # Verifica se o usuário é ativo
        if not user.is_active:
            raise forms.ValidationError("Esta conta foi desativada.", code='inactive')

        # Aqui, insira as regras específicas para o plano de cada usuário
        # Exemplo:
        if hasattr(user, 'profile'):
            tipo_plano = user.profile.tipo_plano  # campo tipo_plano do modelo Profile

            if tipo_plano == 'basico' and not self.allow_basic_user():
                raise forms.ValidationError("Usuários do plano básico têm acesso restrito.", code='basic_plan_restricted')
                
            elif tipo_plano == 'mensal' and not self.allow_monthly_user():
                raise forms.ValidationError("Usuários do plano mensal têm acesso restrito.", code='monthly_plan_restricted')
                
    def allow_basic_user(self):
        # Adicione regras específicas para usuários do plano básico
        return True
    
    def allow_monthly_user(self):
        # Adicione regras específicas para usuários do plano mensal
        return True
