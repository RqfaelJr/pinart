from django.contrib import admin
from eventos.models import Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', )
    
    list_filter = ('nome',)
    
    search_fields = ('nome',)
    