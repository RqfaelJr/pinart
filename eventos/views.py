from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Evento
from .forms import LocalForm, MidiaForm, CategoriaForm, EventoForm, AvaliacaoForm
from pessoas.decorators import organizador_required, participante_required
from django.contrib.auth.decorators import login_required

def _get_next_url(request, default_name='home'):
    return request.POST.get('next') or request.GET.get('next') or reverse(default_name)

def home(request):
    eventos = Evento.objects.all().order_by('data_hora_inicio')
    return render(request, 'index.html', {'eventos': eventos})

@login_required
@organizador_required
def create_local(request):
    next_url = _get_next_url(request)
    if request.method == 'POST':
        form = LocalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next_url)
    else:
        form = LocalForm()
    return render(request, 'form.html', {'form': form, 'title': 'Criar Local', 'next': next_url})

@login_required
@organizador_required
def create_midia(request):
    next_url = _get_next_url(request)
    if request.method == 'POST':
        form = MidiaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next_url)
    else:
        form = MidiaForm()
    return render(request, 'form.html', {'form': form, 'title': 'Criar Mídia', 'next': next_url})

@login_required
@organizador_required
def create_categoria(request):
    next_url = _get_next_url(request)
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next_url)
    else:
        form = CategoriaForm()
    return render(request, 'form.html', {'form': form, 'title': 'Criar Categoria', 'next': next_url})

@login_required
@organizador_required
def create_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user.pessoa
            evento.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = EventoForm()
    return render(request, 'form.html', {
        'form': form,
        'title': 'Criar Evento',
        'next_local': reverse('create_local') + f'?next={request.path}',
        'next_categoria': reverse('create_categoria') + f'?next={request.path}',
        'next_midia': reverse('create_midia') + f'?next={request.path}',
    })

@login_required 
@participante_required
def create_avaliacao(request):
    next_url = _get_next_url(request)
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.pessoa = request.user.pessoa
            avaliacao.save()
            return redirect(next_url)
    else:
        form = AvaliacaoForm()
    return render(request, 'form.html', {'form': form, 'title': 'Criar Avaliação', 'next': next_url})