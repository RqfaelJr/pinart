from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import UserForm, PessoaForm, EnderecoForm

def cadastro(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        pessoa_form = PessoaForm(request.POST)

        if user_form.is_valid() and pessoa_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            is_org = user_form.cleaned_data.get('eh_organizador')
            
            if is_org:
                grupo = Group.objects.get(name='Organizador')
            else:
                grupo = Group.objects.get(name='Participante')
            
            user.groups.add(grupo)

            pessoa = pessoa_form.save(commit=False)
            pessoa.user = user
            pessoa.save()

            return redirect('login')

    else:
        user_form = UserForm()
        pessoa_form = PessoaForm()

    return render(request, 'cadastro.html', {'user_form': user_form, 'pessoa_form': pessoa_form})
    

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
