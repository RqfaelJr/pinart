from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import UserForm, PessoaForm, EnderecoForm, UserUpdateForm, PessoaUpdateForm
from django.contrib.auth.decorators import login_required

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

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PessoaUpdateForm(request.POST, request.FILES, instance=request.user.pessoa)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('perfil')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PessoaUpdateForm(instance=request.user.pessoa)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'editar_perfil.html', context)