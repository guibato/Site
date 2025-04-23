from django import forms
from .models import Imovel, FotoImovel
from django.forms import inlineformset_factory

class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = '__all__'

# Formulário para cada foto individual
class FotoImovelForm(forms.ModelForm):
    class Meta:
        model = FotoImovel
        fields = ['imagem', 'principal']

# Formset para gerenciar múltiplas fotos de um imóvel
FotoImovelFormSet = inlineformset_factory(
    Imovel,
    FotoImovel,
    form=FotoImovelForm,
    fields=('imagem', 'principal'),
    extra=1,
    can_delete=True,
    max_num=12  # Limite máximo de 12 fotos
)