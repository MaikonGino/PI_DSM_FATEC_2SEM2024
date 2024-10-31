#permissões específicas e restrições de visualização, 
from django.shortcuts import redirect
from django.urls import reverse

class PlanoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se o usuário está autenticado e aplica as regras de plano
        if request.user.is_authenticated:
            tipo_plano = request.user.profile.tipo_plano  # Campo do modelo de perfil
            if tipo_plano == 'basico':
                # Redireciona usuários básicos conforme as regras
                return redirect(reverse('restricao_basico'))
        
        response = self.get_response(request)
        return response
