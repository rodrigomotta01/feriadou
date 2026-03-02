from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Solicitacao

class FeriadoRequestForm(forms.ModelForm):
    estado = forms.CharField(label="Sigla do Estado", max_length=2)
    class Meta:
        model = Solicitacao
        fields = ['name', 'day', 'month', 'escopo', 'estado', 'municipio']
        labels = {
            'name' : 'Nome do Feriado',
            'day' : 'Dia',
            'month' : 'Mês',
            'escopo' : "Escopo do Feriado",
            'municipio': "Municipio do Feriado"
        }

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
        if commit:
            user.save()
        return user
