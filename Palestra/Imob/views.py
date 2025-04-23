from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Imovel, FotoImovel
from .forms import ImovelForm, FotoImovelForm
from django.contrib.auth import authenticate, login, logout
from django.forms import modelformset_factory

def home(request):
    # Filtros para buscar imóveis com base nos parâmetros da URL
    objetivo = request.GET.get('objetivo')
    endereco = request.GET.get('endereco')
    tipo = request.GET.get('tipo')
    preco_maximo = request.GET.get('preco')

    # Consulta inicial para buscar todos os imóveis
    imoveis = Imovel.objects.all().prefetch_related('fotos').order_by('-destaque', '-data_cadastro')

    # Aplicar filtros
    if objetivo:
        imoveis = imoveis.filter(negocio__iexact=objetivo)
    if endereco:
        imoveis = imoveis.filter(cidade__icontains=endereco)
    if tipo:
        imoveis = imoveis.filter(tipo__iexact=tipo)
    if preco_maximo:
        if '-' in preco_maximo:
            min_val, max_val = map(float, preco_maximo.split('-'))
            imoveis = imoveis.filter(preco__gte=min_val, preco__lte=max_val)
        elif preco_maximo.endswith('+'):
            min_val = float(preco_maximo.replace('+', ''))
            imoveis = imoveis.filter(preco__gte=min_val)

    # Renderizar o template com os imóveis filtrados
    return render(request, 'index.html', {'imoveis': imoveis})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')

@login_required
def dashboard(request):
    imoveis = Imovel.objects.all().order_by('-data_cadastro')
    return render(request, 'imoveis/dashboard.html', {'imoveis': imoveis})

def lista_imoveis(request):
    # Carrega os imóveis junto com suas fotos relacionadas em uma única consulta
    imoveis = Imovel.objects.all().prefetch_related('fotos').order_by('-destaque', '-data_cadastro')
    
    # Filtros
    tipo = request.GET.get('tipo')
    negocio = request.GET.get('negocio')
    cidade = request.GET.get('cidade')
    
    if tipo:
        imoveis = imoveis.filter(tipo=tipo.lower())  # Convertendo para minúsculas para compatibilidade
    if negocio:
        imoveis = imoveis.filter(negocio=negocio.lower())  # Convertendo para minúsculas
    if cidade:
        imoveis = imoveis.filter(cidade__icontains=cidade)
    
    return render(request, 'imoveis/lista_imoveis.html', {'imoveis': imoveis})

def detalhes_imovel(request, imovel_id):
    imovel = get_object_or_404(Imovel, id=imovel_id)
    return render(request, 'detalhes_imovel.html', {'imovel': imovel})

@login_required
def cadastrar_imovel(request):
    FotoFormSet = modelformset_factory(FotoImovel, form=FotoImovelForm, extra=1, can_delete=True)

    if request.method == "POST":
        form = ImovelForm(request.POST, request.FILES)
        formset = FotoFormSet(request.POST, request.FILES, queryset=FotoImovel.objects.none())

        if form.is_valid() and formset.is_valid():
            # Salva o imóvel principal
            imovel = form.save()

            # Associa cada foto ao imóvel recém-criado
            for f in formset:
                foto = f.save(commit=False)
                foto.imovel = imovel  # Define o relacionamento com o imóvel
                foto.save()

            messages.success(request, 'Imóvel cadastrado com sucesso!')
            return redirect('lista_imoveis')
        else:
            messages.error(request, 'Houve erros no formulário.')
    else:
        form = ImovelForm()
        formset = FotoFormSet(queryset=FotoImovel.objects.none())

    return render(request, 'imoveis/cadastrar_imovel.html', {
        'form': form,
        'formset': formset
    })


@login_required
def editar_imovel(request, imovel_id):
    imovel = get_object_or_404(Imovel, pk=imovel_id)
    FotoFormSet = modelformset_factory(FotoImovel, form=FotoImovelForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = ImovelForm(request.POST, request.FILES, instance=imovel)
        formset = FotoFormSet(request.POST, request.FILES, queryset=FotoImovel.objects.filter(imovel=imovel))

        if form.is_valid() and formset.is_valid():
            # Salva o imóvel principal
            form.save()

            # Atualiza ou cria novas fotos associadas ao imóvel
            for f in formset:
                if f.cleaned_data.get('DELETE'):  # Se a foto foi marcada para exclusão
                    continue
                foto = f.save(commit=False)
                foto.imovel = imovel  # Define o relacionamento com o imóvel
                foto.save()

            messages.success(request, 'Imóvel atualizado com sucesso!')
            return redirect('lista_imoveis')
        else:
            messages.error(request, 'Houve erros no formulário.')
    else:
        form = ImovelForm(instance=imovel)
        formset = FotoFormSet(queryset=FotoImovel.objects.filter(imovel=imovel))

    return render(request, 'imoveis/editar_imovel.html', {
        'form': form,
        'formset': formset,
        'imovel': imovel,
    })

@login_required
def excluir_imovel(request, imovel_id):
    imovel = get_object_or_404(Imovel, id=imovel_id)
    
    if request.method == 'POST':
        imovel.delete()
        messages.success(request, 'Imóvel excluído com sucesso!')
        return redirect('dashboard')
    
    return render(request, 'imoveis/excluir_imovel.html', {'imovel': imovel})
    