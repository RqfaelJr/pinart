from django.contrib import admin

from .models import Notificacao

# --- Configuração para Notificações ---
@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'pessoa', 'tipo', 'lida', 'data_hora', 'evento')
    
    # Filtros laterais
    list_filter = ('tipo', 'lida', 'data_hora')
    
    # Barra de pesquisa 
    # OBS: Se 'Pessoa' tiver um campo 'nome', use 'pessoa__nome'. 
    # Se for o User padrão do Django, use 'pessoa__username'.
    search_fields = ('titulo', 'mensagem', 'pessoa__nome')
    
    # Campos somente leitura
    readonly_fields = ('data_hora',)