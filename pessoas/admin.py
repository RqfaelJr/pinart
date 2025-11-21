from django.contrib import admin

from .models import Notificacao

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'pessoa', 'tipo', 'lida', 'data_hora', 'evento')

    list_filter = ('tipo', 'lida', 'data_hora')
    
    search_fields = ('titulo', 'mensagem', 'pessoa__nome')

    readonly_fields = ('data_hora',)