from django import forms 
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}), validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs= {'class': 'input'}))
    
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone', 'password', 'confirm_password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'phone': forms.TextInput(attrs={'class': 'input'}),
        }
        
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem.")
        return confirm_password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password']) 
        if commit:
            user.save()
        return user
    
    
