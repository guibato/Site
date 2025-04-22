from django.db import models

class Imovel(models.Model):
    TIPO_CHOICES = [
        ('Casa', 'Casa'),
        ('Apartamento', 'Apartamento'),
        ('Terreno', 'Terreno'),
        ('Comercial', 'Comercial'),
    ]

    STATUS_CHOICES = [
        ('Disponível', 'Disponível'),
        ('Alugado/Vendido', 'Alugado/Vendido'),
    ]

    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField()
    endereco = models.CharField(max_length=300)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quartos = models.PositiveIntegerField()
    banheiros = models.PositiveIntegerField()
    area = models.PositiveIntegerField(help_text="Área em metros quadrados")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponível')
    imagem = models.ImageField(upload_to='imoveis/', blank=True, null=True)

    def __str__(self):
        return self.titulo