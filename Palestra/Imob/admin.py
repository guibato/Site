from django.contrib import admin
from .models import Imovel, FotoImovel

class FotoImovelInline(admin.TabularInline):
    model = FotoImovel
    extra = 1

@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'negocio', 'preco']  # Remove 'status'
    list_filter = ['tipo', 'negocio', 'destaque']
    search_fields = ['titulo', 'endereco', 'bairro', 'cidade']
    inlines = [FotoImovelInline]

@admin.register(FotoImovel)
class FotoImovelAdmin(admin.ModelAdmin):
    list_display = ['imovel', 'principal']
    list_filter = ['principal']