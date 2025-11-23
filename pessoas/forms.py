from django import forms
from django.contrib.auth.models import User
from .models import Pessoa

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    eh_organizador = forms.BooleanField(
        required=False, 
        label="Sou um organizador de eventos",
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-custom'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['cpf', 'telefone', 'data_nascimento', 'endereco']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Pessoa.endereco.field.related_model
        fields = ['rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(attrs={'placeholder': 'Seu usuário'})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Sua senha'})
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class PessoaUpdateForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['telefone', 'endereco']
