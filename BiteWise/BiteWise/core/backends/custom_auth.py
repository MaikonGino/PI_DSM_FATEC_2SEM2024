from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class TestLoginBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Se o usuário já existir, retorna o usuário
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            # Se o usuário não existir, cria um usuário com a senha fornecida
            user = User(username=username)
            user.set_password(password)  # Define a senha
            user.save()  # Salva o novo usuário no banco
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
