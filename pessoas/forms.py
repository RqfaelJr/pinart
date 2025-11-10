from django import forms
from django.contrib.auth.models import User
from .models import Pessoa

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['cpf', 'telefone', 'data_nascimento', 'endereco']

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Pessoa.endereco.field.related_model
        fields = ['rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']
