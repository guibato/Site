from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class Proprietario(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    documento = models.CharField(max_length=20, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Proprietário'
        verbose_name_plural = 'Proprietários'


class Imovel(models.Model):
    class TipoImovel(models.TextChoices):
        CASA = 'CASA', 'Casa'
        APARTAMENTO = 'APARTAMENTO', 'Apartamento'
        TERRENO = 'TERRENO', 'Terreno'
        SALA_COMERCIAL = 'SALA COMERCIAL', 'Sala Comercial'
        GALPAO = 'GALPÃO', 'Galpão'
        OUTRO = 'OUTRO', 'Outro'
    
    class Finalidade(models.TextChoices):
        VENDA = 'venda', 'Venda'
        ALUGUEL = 'aluguel', 'Aluguel'
        AMBOS = 'ambos', 'Venda e Aluguel'
    
    # Identificação do imóvel
    titulo = models.CharField(max_length=200, default='', help_text='Título para exibição do imóvel')
    tipo = models.CharField(
        max_length=20,
        choices=TipoImovel.choices,
        default=TipoImovel.CASA,
        verbose_name='Tipo do Imóvel'
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição',
        help_text='Informações complementares sobre o imóvel'
    )
    proprietario = models.ForeignKey(
        Proprietario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='imoveis'
    )
    
    # Endereço
    endereco = models.CharField(max_length=255, verbose_name='Endereço')
    numero = models.CharField(max_length=10, blank=True, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Características físicas
    finalidade = models.CharField(max_length=10, choices=Finalidade.choices)
    quartos = models.PositiveIntegerField(default=0)
    suites = models.PositiveIntegerField(default=0)
    banheiros = models.PositiveIntegerField(default=0)
    vagas_garagem = models.PositiveIntegerField(default=0, verbose_name='Vagas na garagem')
    area_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='Área total (m²)')
    area_privativa = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='Área privativa (m²)')
    andar = models.PositiveIntegerField(null=True, blank=True, help_text='Preencher se for apartamento ou sala')
    mobiliado = models.BooleanField(default=False)
    aceita_pets = models.BooleanField(default=False)
    
    # Status
    ativo = models.BooleanField(default=True)
    destaque = models.BooleanField(default=False)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    # Preço
    preco = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        help_text='Preço de venda'
    )
    aluguel = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        help_text='Valor do aluguel mensal'
    )
    condominio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    iptu = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'
        ordering = ['-destaque', '-data_cadastro']
    
    def __str__(self):
        return f'{self.get_tipo_display()} - {self.endereco}, {self.numero or "s/n"} - {self.cidade}/{self.estado}'
    
    def get_absolute_url(self):
        return reverse('detalhe_imovel', args=[str(self.slug)])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.titulo if self.titulo else f"{self.get_tipo_display()} {self.endereco} {self.bairro}"
            self.slug = slugify(base)
            
            # Verifica se já existe um slug igual
            n = 1
            while Imovel.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(base)}-{n}"
                n += 1
                
        # Valida campos de preço conforme a finalidade
        if self.finalidade == self.Finalidade.VENDA and not self.preco:
            self.preco = 0
        elif self.finalidade == self.Finalidade.ALUGUEL and not self.aluguel:
            self.aluguel = 0
                
        super().save(*args, **kwargs)
    
    def formatar_valor(self, valor):
        if valor is None or valor == 0:
            return "Não informado"
        valor_str = f"{valor:,.2f}"
        valor_str = valor_str.replace(".", "X")
        valor_str = valor_str.replace(",", ".")
        valor_str = valor_str.replace("X", ",")
        return f"R$ {valor_str}"
    
    def preco_formatado(self):
        return self.formatar_valor(self.preco)
    
    def aluguel_formatado(self):
        return self.formatar_valor(self.aluguel)
    
    def condominio_formatado(self):
        return self.formatar_valor(self.condominio)
    
    def iptu_formatado(self):
        return self.formatar_valor(self.iptu)
    
    @property
    def foto_principal(self):
        foto = self.fotos.filter(principal=True).first()
        if not foto:
            foto = self.fotos.first()
        return foto


class FotoImovel(models.Model):
    imovel = models.ForeignKey(Imovel, related_name='fotos', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='imoveis/')
    principal = models.BooleanField(default=False)
    titulo = models.CharField(max_length=100, blank=True)
    ordem = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'
        ordering = ['ordem', '-principal']
    
    def __str__(self):
        return f"Foto de {self.imovel}" if not self.titulo else self.titulo
    
    def save(self, *args, **kwargs):
        # Se esta foto for marcada como principal, desmarca as outras
        if self.principal:
            FotoImovel.objects.filter(imovel=self.imovel, principal=True).update(principal=False)
        super().save(*args, **kwargs)


class Comodidade(models.Model):
    nome = models.CharField(max_length=100)
    icone = models.CharField(max_length=50, blank=True, help_text="Classe CSS do ícone")
    
    class Meta:
        verbose_name = 'Comodidade'
        verbose_name_plural = 'Comodidades'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class ImovelComodidade(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name='comodidades')
    comodidade = models.ForeignKey(Comodidade, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Comodidade do Imóvel'
        verbose_name_plural = 'Comodidades do Imóvel'
        unique_together = ('imovel', 'comodidade')
    
    def __str__(self):
        return f"{self.comodidade.nome} - {self.imovel}"


class Contato(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name='contatos', null=True, blank=True)
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    respondido = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
        ordering = ['-data']
    
    def __str__(self):
        return f"Contato de {self.nome} - {self.data.strftime('%d/%m/%Y')}"