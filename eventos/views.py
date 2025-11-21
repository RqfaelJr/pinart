from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Categoria, Evento
from pessoas.models import Notificacao
from .forms import LocalForm, MidiaForm, CategoriaForm, EventoForm, AvaliacaoForm
from pessoas.decorators import organizador_required, participante_required
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

def _get_next_url(request, default_name='home'):
    return request.POST.get('next') or request.GET.get('next') or reverse(default_name)

def home(request):
    categoria = request.GET.get('categoria')


    categorias = Categoria.objects.all()


    eventos = Evento.objects.all()
    if categoria:
        eventos = eventos.filter(categorias__id=categoria)


    return render(request, 'index.html', {
    'eventos': eventos,
    'categorias': categorias,
    'categoria_selecionada': int(categoria) if categoria else None
})

@login_required
@organizador_required
def create_local(request):
    if request.method == 'POST':
        # Verifica se é uma requisição AJAX/JSON do Modal
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
            form = LocalForm(data)
            if form.is_valid():
                local = form.save()
                # Retorna JSON para o JavaScript do modal
                return JsonResponse({
                    'id': local.id,
                    'nome': local.nome,
                    'message': 'Local criado com sucesso!'
                })
            else:
                return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = LocalForm()
    
    return render(request, 'modal_local.html', {'form': form})

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

@login_required
def lista_notificacoes(request):
    notificacoes = Notificacao.objects.filter(pessoa=request.user.pessoa)
    
    return render(request, 'notificacoes.html', {
        'notificacoes': notificacoes
    })

@login_required
def marcar_todas_lidas(request):
    if request.method == 'POST':
        Notificacao.objects.filter(pessoa=request.user.pessoa, lida=False).update(lida=True)
    
    return redirect('lista_notificacoes')