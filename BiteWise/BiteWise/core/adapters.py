from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # Impede a criação de usuário com o campo 'username' no cadastro
        return True

    def save_user(self, request, user, form, commit=True):
        # Garantir que o email seja usado como 'username' no cadastro
        user.email = form.cleaned_data.get('email')
        user.username = form.cleaned_data.get('email')  # Use o email como 'username' se necessário
        return super().save_user(request, user, form, commit)