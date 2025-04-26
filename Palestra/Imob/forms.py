from django import forms
from django.forms import inlineformset_factory
from .models import Imovel, FotoImovel, Proprietario, Comodidade, ImovelComodidade, Contato
from .widgets import MultipleFileField, MultipleFileInput  # Add MultipleFileInput here

class ProprietarioForm(forms.ModelForm):
    class Meta:
        model = Proprietario
        fields = ['nome', 'telefone', 'email', 'documento', 'observacoes', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'telefone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': '(XX) XXXXX-XXXX'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}),
            'documento': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'CPF ou CNPJ'}),
            'observacoes': forms.Textarea(attrs={'class': 'w-full h-24 p-2 border rounded'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-blue-600'}),
        }


class ImovelForm(forms.ModelForm):
    # Use o novo campo aqui
    fotos_multiplas = MultipleFileField(
        required=False,
        label="Adicionar fotos",
        widget=MultipleFileInput(attrs={'class': 'hidden'})
    )
    
    # Campo para comodidades (checkboxes)
    comodidades = forms.ModelMultipleChoiceField(
        queryset=Comodidade.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
        required=False,
        label="Comodidades"
    )
    
    class Meta:
        model = Imovel
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Título atrativo para o imóvel'
            }),
            'tipo': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'finalidade': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'proprietario': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'descricao': forms.Textarea(attrs={
                'class': 'w-full h-32 p-2 border rounded',
                'placeholder': 'Descreva os principais atrativos do imóvel...'
            }),
            'endereco': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'numero': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'complemento': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'bairro': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'cidade': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'estado': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'maxlength': 2}),
            'cep': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': '00000-000'}),
            'latitude': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'step': 'any'}),

            'quartos': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'min': 0}),
            'suites': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'min': 0}),
            'banheiros': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'min': 0}),
            'vagas_garagem': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'min': 0}),
            'area_total': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'step': '0.01', 'min': 0}),
            'area_privativa': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'step': '0.01', 'min': 0}),
            'andar': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'min': 0}),
            
            'mobiliado': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-blue-600'}),
            'aceita_pets': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-blue-600'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-blue-600'}),
            'destaque': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-blue-600'}),
            
            'preco': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'step': '0.01', 'min': 0}),
            'aluguel': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'step': '0.01', 'min': 0}),
            'condominio': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'step': '0.01', 'min': 0, 'required': False}),
            'iptu': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'step': '0.01', 'min': 0, 'required': False}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Torna os campos opcionais inicialmente, serão validados no clean
        self.fields['preco'].required = False
        self.fields['aluguel'].required = False
        
        # Se estamos editando um imóvel existente, carregamos as comodidades
        if self.instance.pk:
            self.initial['comodidades'] = self.instance.comodidades.values_list('comodidade', flat=True)
    
    def clean(self):
        cleaned_data = super().clean()
        finalidade = cleaned_data.get('finalidade')
        preco = cleaned_data.get('preco')
        aluguel = cleaned_data.get('aluguel')
        
        if finalidade == Imovel.Finalidade.VENDA and not preco:
            self.add_error('preco', 'O preço de venda é obrigatório para imóveis à venda.')
        
        if finalidade == Imovel.Finalidade.ALUGUEL and not aluguel:
            self.add_error('aluguel', 'O valor do aluguel é obrigatório para imóveis para locação.')
        
        if finalidade == Imovel.Finalidade.AMBOS:
            if not preco:
                self.add_error('preco', 'O preço de venda é obrigatório quando a finalidade é ambos.')
            if not aluguel:
                self.add_error('aluguel', 'O valor do aluguel é obrigatório quando a finalidade é ambos.')
        
        return cleaned_data
    
    def save(self, commit=True):
        imovel = super().save(commit=commit)
        
        if commit:
            # Salva as comodidades selecionadas
            comodidades = self.cleaned_data.get('comodidades', [])
            
            # Remove todas as comodidades existentes
            ImovelComodidade.objects.filter(imovel=imovel).delete()
            
            # Adiciona as comodidades selecionadas
            for comodidade in comodidades:
                ImovelComodidade.objects.create(imovel=imovel, comodidade=comodidade)
        
        return imovel


class FotoImovelForm(forms.ModelForm):
    class Meta:
        model = FotoImovel
        fields = ['imagem', 'titulo', 'principal', 'ordem']
        widgets = {
            'imagem': forms.ClearableFileInput(attrs={'class': 'p-2 border rounded'}),
            'titulo': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'principal': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-blue-600'}),
            'ordem': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'min': 0}),
        }


# Formset para gerenciar múltiplas fotos de um imóvel
FotoImovelFormSet = inlineformset_factory(
    Imovel,
    FotoImovel,
    form=FotoImovelForm,
    fields=('imagem', 'titulo', 'principal', 'ordem'),
    extra=1,
    can_delete=True,
    max_num=20  # Limite máximo de 20 fotos
)


class ComodidadeForm(forms.ModelForm):
    class Meta:
        model = Comodidade
        fields = ['nome', 'icone']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'icone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'fa-swimming-pool'}),
        }


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'telefone', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}),
            'telefone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': '(XX) XXXXX-XXXX'}),
            'mensagem': forms.Textarea(attrs={'class': 'w-full h-32 p-2 border rounded'}),
        }


class ImovelBuscaForm(forms.Form):
    ORDEM_CHOICES = [
        ('recentes', 'Mais recentes'),
        ('preco_asc', 'Menor preço'),
        ('preco_desc', 'Maior preço'),
        ('area_asc', 'Menor área'),
        ('area_desc', 'Maior área'),
    ]
    
    tipo = forms.ChoiceField(
        choices=[('', 'Todos os tipos')] + list(Imovel.TipoImovel.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full p-2 border rounded'})
    )
    finalidade = forms.ChoiceField(
        choices=[('', 'Todas as finalidades')] + list(Imovel.Finalidade.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full p-2 border rounded'})
    )
    cidade = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Cidade'})
    )
    bairro = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Bairro'})
    )
    quartos_min = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Quartos (mín)'})
    )
    preco_min = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Preço mínimo'})
    )
    preco_max = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Preço máximo'})
    )
    area_min = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Área mínima (m²)'})
    )
    comodidades = forms.ModelMultipleChoiceField(
        queryset=Comodidade.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox h-5 w-5 text-blue-600'})
    )
    ordenacao = forms.ChoiceField(
        choices=ORDEM_CHOICES,
        required=False,
        initial='recentes',
        widget=forms.Select(attrs={'class': 'w-full p-2 border rounded'})
    )