from django.contrib import admin

from eventos.models import Categoria

# --- Configuração para Notificações ---
@admin.register(Categoria)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', )
    
    list_filter = ('nome',)
    
    search_fields = ('nome',)
    