from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label = 'Email')

class SignUpForm(UserCreationForm):
    username = forms.EmailField(label = 'Email')
    password1 = forms.CharField(label = "Senha")
    password2 = forms.CharField(label = "Confirmar Senha")

    class Meta:
        model = User
        fields = ("first_name", "username")
        labels = {
            "first_name": "Primeiro Nome",
            "username": "E-mail"
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.username
        # alterar algo no user aqui se precisar
        if commit:
            user.save()
        return user

class UsernamePasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        # Busca o e-mail no username, e não no campo e-mail(não está sendo usado)
        active_users = User._default_manager.filter(username__iexact=email, is_active=True)
        return (u for u in active_users)