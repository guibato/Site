from django.db import models
from django.urls import reverse
from django.utils.formats import number_format

class Imovel(models.Model):
    TIPO_CHOICES = [
        ('casa', 'Casa'),
        ('apartamento', 'Apartamento'),
        ('terreno', 'Terreno'),
        ('comercial', 'Comercial'),
        ('rural', 'Rural'),
    ]
    
    NEGOCIO_CHOICES = [
        ('venda', 'Venda'),
        ('aluguel', 'Aluguel'),
    ]
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('vendido', 'Vendido'),
        ('alugado', 'Alugado'),
        ('reservado', 'Reservado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    negocio = models.CharField(max_length=10, choices=NEGOCIO_CHOICES)
    preco = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Preço")
    area = models.DecimalField(max_digits=8, decimal_places=2)
    quartos = models.PositiveIntegerField(default=0)
    banheiros = models.PositiveIntegerField(default=0)
    vagas_garagem = models.PositiveIntegerField(default=0)
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=255, blank=True, null=True)
    complemento = models.CharField(max_length=255, blank=True, null=True)  # Novo campo para complemento
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    descricao = models.TextField()
    destaque = models.BooleanField(default=False)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('detalhe_imovel', args=[str(self.id)])
    
    def preco_formatado(self):
        # Formata o número com pontos como separadores de milhar e vírgula como separador decimal
        preco_str = f"{self.preco:,.2f}"  # Formata com pontos e vírgulas
        preco_str = preco_str.replace(".", "X")  # Substitui o ponto por um marcador temporário
        preco_str = preco_str.replace(",", ".")  # Substitui a vírgula por ponto
        preco_str = preco_str.replace("X", ",")  # Substitui o marcador temporário por vírgula
        return f"R$ {preco_str}"



class FotoImovel(models.Model):
    imovel = models.ForeignKey(Imovel, related_name='fotos', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='imoveis/')
    principal = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Foto de {self.imovel.titulo}"