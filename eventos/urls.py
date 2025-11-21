from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('local/new/', views.create_local, name='create_local'),
    path('midia/new/', views.create_midia, name='create_midia'),
    path('categoria/new/', views.create_categoria, name='create_categoria'),
    path('evento/new/', views.create_evento, name='create_evento'),
    path('avaliacao/new/', views.create_avaliacao, name='create_avaliacao'),
    path('notificacoes/', views.lista_notificacoes, name='lista_notificacoes'),
    path('notificacoes/marcar_todas_lidas/', views.marcar_todas_lidas, name='marcar_todas_lidas'),
    path('evento/<int:evento_id>/', views.detalhe_evento, name='detalhe_evento'),
    path('perfil/', views.perfil, name='perfil'),
    path('listar_eventos/', views.listar_eventos, name='lista_eventos'),
    path('mapa/', views.mapa, name='mapa'),
]