from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Imovel, FotoImovel, Proprietario, Comodidade, ImovelComodidade  
from .forms import ImovelForm, FotoImovelForm, ProprietarioForm, ComodidadeForm
from django.contrib.auth import authenticate, login, logout
from django.forms import modelformset_factory
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


def home(request):
    OBJETIVO_MAP = {
        'comprar': 'venda',
        'compra': 'venda',
        'venda': 'venda',
        'alugar': 'aluguel',
        'aluguel': 'aluguel',
        'ambos': 'ambos',
        'todos': '',  # caso queira listar todos
    }

    objetivo = request.GET.get('objetivo')
    endereco = request.GET.get('endereco')
    tipo = request.GET.get('tipo')
    preco_maximo = request.GET.get('preco')

    imoveis = Imovel.objects.all().prefetch_related('fotos').order_by('-destaque', '-data_cadastro')

    # Aplica o filtro por finalidade traduzido
    if objetivo:
        objetivo_valor = OBJETIVO_MAP.get(objetivo.lower())
        if objetivo_valor:
            imoveis = imoveis.filter(finalidade=objetivo_valor)

    if endereco:
        imoveis = imoveis.filter(cidade__icontains=endereco)

    if tipo:
        imoveis = imoveis.filter(tipo__iexact=tipo)

    if preco_maximo:
        if '-' in preco_maximo:
            try:
                min_val, max_val = map(float, preco_maximo.split('-'))
                imoveis = imoveis.filter(preco__gte=min_val, preco__lte=max_val)
            except ValueError:
                pass
        elif preco_maximo.endswith('+'):
            try:
                min_val = float(preco_maximo.replace('+', ''))
                imoveis = imoveis.filter(preco__gte=min_val)
            except ValueError:
                pass

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
    if request.method == "POST":
        form = ImovelForm(request.POST, request.FILES)
        if form.is_valid():
            imovel = form.save()
            messages.success(request, 'Imóvel cadastrado com sucesso!')
            return redirect('upload_fotos_imovel', imovel_id=imovel.id)
        else:
            messages.error(request, 'Houve erros no formulário.')
    else:
        form = ImovelForm()

    return render(request, 'imoveis/cadastrar_imovel.html', {'form': form})

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

def cadastrar_proprietario(request):
    """View for registering a new property owner."""
    if request.method == 'POST':
        form = ProprietarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proprietário cadastrado com sucesso!')
            return redirect('listar_proprietarios')
        else:
            messages.error(request, 'Erro ao cadastrar proprietário. Por favor, verifique os dados.')
    else:
        form = ProprietarioForm()
    
    return render(request, 'cadastrar_proprietario.html', {'form': form})

def listar_proprietarios(request):
    """View for listing all property owners."""
    proprietarios_list = Proprietario.objects.all().order_by('nome')
    
    # Paginação
    paginator = Paginator(proprietarios_list, 10)  # 10 proprietários por página
    page = request.GET.get('page')
    proprietarios = paginator.get_page(page)
    
    return render(request, 'prop/lista_prop.html', {'proprietarios': proprietarios})

def editar_proprietario(request, id):
    """View for editing a property owner."""
    proprietario = get_object_or_404(Proprietario, id=id)
    
    if request.method == 'POST':
        form = ProprietarioForm(request.POST, instance=proprietario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proprietário atualizado com sucesso!')
            return redirect('prop/lista_prop')
        else:
            messages.error(request, 'Erro ao atualizar proprietário. Por favor, verifique os dados.')
    else:
        form = ProprietarioForm(instance=proprietario)
    
    return render(request, 'prop/editar_prop.html', {'form': form, 'proprietario': proprietario})

def visualizar_proprietario(request, id):
    """View for viewing a property owner's details."""
    proprietario = get_object_or_404(Proprietario, id=id)
    return render(request, 'prop/visualizar_prop.html', {'proprietario': proprietario})

def excluir_proprietario(request, id):
    """View for deleting a property owner."""
    proprietario = get_object_or_404(Proprietario, id=id)
    
    if request.method == 'POST':
        """View for viewing a property owner's details."""
    proprietario = get_object_or_404(Proprietario, id=id)
    return render(request, 'prop/visualizar_prop.html', {'proprietario': proprietario})

@login_required
def upload_fotos_imovel(request, imovel_id):
    imovel = get_object_or_404(Imovel, id=imovel_id)
    return render(request, 'imoveis/upload_fotos.html', {'imovel': imovel})

from django.http import JsonResponse

@csrf_exempt
@login_required
def upload_foto_ajax(request):
    if request.method == "POST":
        imovel_id = request.POST.get("imovel_id")
        imagem = request.FILES.get("file")

        if not imovel_id or not imagem:
            return JsonResponse({'error': 'Dados incompletos'}, status=400)

        imovel = get_object_or_404(Imovel, id=imovel_id)
        foto = FotoImovel(imovel=imovel, imagem=imagem)
        foto.save()

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Método inválido'}, status=405)
