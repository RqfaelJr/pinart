from pyexpat.errors import messages
from random import random
import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Categoria, Evento
from pessoas.models import Notificacao
from pessoas.forms import EnderecoForm
from .forms import LocalForm, MidiaForm, CategoriaForm, EventoForm, AvaliacaoForm
from pessoas.decorators import organizador_required, participante_required
from django.contrib.auth.decorators import login_required
import json
from django.db import transaction
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
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        try:
            data = json.loads(request.body)
            local_data = data.get('local')
            endereco_data = data.get('endereco')

            with transaction.atomic():
                endereco_form = EnderecoForm(endereco_data)
                if endereco_form.is_valid():
                    endereco = endereco_form.save()
                else:
                    return JsonResponse({'errors': endereco_form.errors}, status=400)

                local_form = LocalForm(local_data)
                if local_form.is_valid():
                    local = local_form.save(commit=False)
                    local.endereco = endereco
                    
                    
                    lat, lon = buscar_coordenadas(endereco)
                    if lat and lon:
                        local.latitude = lat
                        local.longitude = lon
                    
                    local.save()
                    
                    return JsonResponse({
                        'id': local.id, 
                        'nome': local.nome,
                        'message': 'Local criado e localizado com sucesso!'
                    })
                else:
                    return JsonResponse({'errors': local_form.errors}, status=400)
                    
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def buscar_coordenadas(endereco):
    try:
        if (endereco.numero is None):
            query = f"{endereco.rua}, {endereco.bairro}, {endereco.cidade} - {endereco.estado}"
        else:
            query = f"{endereco.rua}, {endereco.numero}, {endereco.bairro}, {endereco.cidade} - {endereco.estado}"
        
        headers = {'User-Agent': 'PinArtApp/1.0 (ribeiro.rafajunior@gmail.com)'}
        
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': query,
            'format': 'json',
            'limit': 1
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        data = response.json()
        
        if data and len(data) > 0:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
            
    except Exception as e:
        print(f"Erro na geocodificação: {e}")
    
    return None, None

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

@login_required
def detalhe_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    return render(request, 'detalhe_evento.html', {
        'evento': evento
    })
@login_required
def perfil(request):
    pessoa = request.user.pessoa
    return render(request, 'perfil.html', {
        'pessoa': pessoa
    })
@login_required
def listar_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'lista_eventos.html', {
        'eventos': eventos
    })

@login_required
def mapa(request):
    eventos = Evento.objects.select_related('local').all()
    
    eventos_list = []
    
    for evento in eventos:

        if not evento.local:
            continue

        # Tenta pegar as coordenadas reais do banco
        lat = getattr(evento.local, 'latitude', None)
        lng = getattr(evento.local, 'longitude', None)
        
        # Caso não existam, usa valores padrão
        if not lat or not lng:
            lat = -28.9355 + random() * 0.1
            lng = -49.4908 + random() * 0.1 
        
        eventos_list.append({
            'id': evento.id,
            'titulo': evento.titulo,
            'lat': float(lat),
            'lng': float(lng),
            'categoria': str(evento.categorias.first()) if evento.categorias.exists() else 'Outros',
            'local_nome': evento.local.nome,
            'data': evento.data_hora_inicio.strftime('%d/%m/%Y às %H:%M'),
            'url': f"/evento/{evento.id}/" # Certifique-se que essa URL existe
        })

    

    return render(request, 'mapa.html', {
        'eventos': eventos, 
        'eventos_json': eventos_list
    })

def confirmar_presenca(request, evento_id):
    pass

@login_required
@participante_required
def comentar_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    form = AvaliacaoForm(request.POST)

    if form.is_valid():
        avaliacao = form.save(commit=False)
        avaliacao.evento = evento
        
        try:
            if hasattr(request.user, 'pessoa'):
                avaliacao.pessoa = request.user.pessoa
            else:
                messages.error(request, 'Você precisa ter um perfil de Pessoa para comentar.')
                return redirect('detalhe_evento', evento_id=evento_id)
        except Exception as e:
             pass

        avaliacao.save()
        messages.success(request, 'Comentário enviado com sucesso!')
    else:
        messages.error(request, 'Erro ao enviar comentário. Verifique os campos.')

    return redirect('detalhe_evento', evento_id=evento_id)