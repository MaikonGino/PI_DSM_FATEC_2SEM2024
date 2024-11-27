from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True

    def save_user(self, request, user, form, commit=True):
        user.email = form.cleaned_data.get('email')
        user.username = form.cleaned_data.get('email')  
        return super().save_user(request, user, form, commit)