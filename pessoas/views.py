from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import UserForm, PessoaForm, EnderecoForm

def cadastrar_organizador(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        pessoa_form = PessoaForm(request.POST)
        print(1)
        if user_form.is_valid() and pessoa_form.is_valid():
            print(2)
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
            print(user_form.errors)
            print(pessoa_form.errors)
    else: 
        print(3)
        user_form = UserForm(request.GET or None)
        pessoa_form = PessoaForm(request.GET or None)


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
        user_form = UserForm(request.GET or None)
        pessoa_form = PessoaForm(request.GET or None)


    return render(request, 'cadastro_participante.html', {
        'user_form': user_form,
        'pessoa_form': pessoa_form
    })

def cadastrar_endereco(request):
    next_url = request.GET.get('next', request.POST.get('next', 'home'))

    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save()
            return redirect(next_url) 
    else:
        form = EnderecoForm()

    return render(request, 'cadastro_endereco.html', {
        'form': form,
        'next': next_url 
    })
