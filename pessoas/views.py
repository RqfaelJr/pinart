from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import UserForm, PessoaForm

def cadastrar_organizador(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        pessoa_form = PessoaForm(request.POST)
        if user_form.is_valid() and pessoa_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            pessoa = pessoa_form.save(commit=False)
            pessoa.user = user
            pessoa.save()

            grupo = Group.objects.get(name='Organizador')
            user.groups.add(grupo)

            return redirect('login')
    else:
        user_form = UserForm()
        pessoa_form = PessoaForm()

    return render(request, 'cadastro_organizador.html', {
        'user_form': user_form,
        'pessoa_form': pessoa_form
    })


def cadastrar_participante(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        pessoa_form = PessoaForm(request.POST)
        if user_form.is_valid() and pessoa_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            pessoa = pessoa_form.save(commit=False)
            pessoa.user = user
            pessoa.save()

            grupo = Group.objects.get(name='Participante')
            user.groups.add(grupo)

            return redirect('login')
    else:
        user_form = UserForm()
        pessoa_form = PessoaForm()

    return render(request, 'cadastro_participante.html', {
        'user_form': user_form,
        'pessoa_form': pessoa_form
    })
