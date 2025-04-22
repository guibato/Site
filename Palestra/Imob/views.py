from django.shortcuts import render, get_object_or_404
from .models import Imovel

# Página inicial: Lista de imóveis
def lista_imoveis(request):
    endereco = request.GET.get('endereco')
    tipo = request.GET.get('tipo')

    # Filtrar imóveis com base nos parâmetros da busca
    imoveis = Imovel.objects.all()
    if endereco:
        imoveis = imoveis.filter(endereco__icontains=endereco)
    if tipo:
        imoveis = imoveis.filter(tipo=tipo)

    # Renderizar o template index.html
    return render(request, 'index.html', {'imoveis': imoveis})

# Detalhes de um imóvel específico
def detalhes_imovel(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk)
    return render(request, 'detalhes_imovel.html', {'imovel': imovel})