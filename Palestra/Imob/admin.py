from django.contrib import admin
from .models import Imovel, FotoImovel

class FotoImovelInline(admin.TabularInline):
    model = FotoImovel
    extra = 1

@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo', 'descricao', 'cidade', 'estado', 'ativo']
    list_filter = ['tipo', 'cidade', 'estado', 'ativo']
    search_fields = ['descricao', 'endereco', 'cidade', 'estado']


@admin.register(FotoImovel)
class FotoImovelAdmin(admin.ModelAdmin):
    list_display = ['imovel', 'principal']
    list_filter = ['principal']