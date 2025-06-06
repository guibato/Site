# Generated by Django 5.2 on 2025-04-24 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comodidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('icone', models.CharField(blank=True, help_text='Classe CSS do ícone', max_length=50)),
            ],
            options={
                'verbose_name': 'Comodidade',
                'verbose_name_plural': 'Comodidades',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Imovel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(default='', help_text='Título para exibição do imóvel', max_length=200)),
                ('tipo', models.CharField(choices=[('CASA', 'Casa'), ('APTO', 'Apartamento'), ('TERRENO', 'Terreno'), ('SALA', 'Sala Comercial'), ('GALPAO', 'Galpão'), ('OUTRO', 'Outro')], default='CASA', max_length=20, verbose_name='Tipo do Imóvel')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('descricao', models.TextField(blank=True, help_text='Informações complementares sobre o imóvel', verbose_name='Descrição')),
                ('endereco', models.CharField(max_length=255, verbose_name='Endereço')),
                ('numero', models.CharField(blank=True, max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=100)),
                ('bairro', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=2)),
                ('cep', models.CharField(blank=True, max_length=10)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('finalidade', models.CharField(choices=[('venda', 'Venda'), ('aluguel', 'Aluguel'), ('ambos', 'Venda e Aluguel')], max_length=10)),
                ('quartos', models.PositiveIntegerField(default=0)),
                ('suites', models.PositiveIntegerField(default=0)),
                ('banheiros', models.PositiveIntegerField(default=0)),
                ('vagas_garagem', models.PositiveIntegerField(default=0, verbose_name='Vagas na garagem')),
                ('area_total', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Área total (m²)')),
                ('area_privativa', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Área privativa (m²)')),
                ('andar', models.PositiveIntegerField(blank=True, help_text='Preencher se for apartamento ou sala', null=True)),
                ('mobiliado', models.BooleanField(default=False)),
                ('aceita_pets', models.BooleanField(default=False)),
                ('ativo', models.BooleanField(default=True)),
                ('destaque', models.BooleanField(default=False)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('preco', models.DecimalField(blank=True, decimal_places=2, help_text='Preço de venda', max_digits=12, null=True)),
                ('aluguel', models.DecimalField(blank=True, decimal_places=2, help_text='Valor do aluguel mensal', max_digits=10, null=True)),
                ('condominio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('iptu', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'verbose_name': 'Imóvel',
                'verbose_name_plural': 'Imóveis',
                'ordering': ['-destaque', '-data_cadastro'],
            },
        ),
        migrations.CreateModel(
            name='Proprietario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('documento', models.CharField(blank=True, max_length=20, null=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Proprietário',
                'verbose_name_plural': 'Proprietários',
            },
        ),
        migrations.CreateModel(
            name='FotoImovel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='imoveis/')),
                ('principal', models.BooleanField(default=False)),
                ('titulo', models.CharField(blank=True, max_length=100)),
                ('ordem', models.PositiveIntegerField(default=0)),
                ('imovel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos', to='Imob.imovel')),
            ],
            options={
                'verbose_name': 'Foto',
                'verbose_name_plural': 'Fotos',
                'ordering': ['ordem', '-principal'],
            },
        ),
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=20)),
                ('mensagem', models.TextField()),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('respondido', models.BooleanField(default=False)),
                ('imovel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contatos', to='Imob.imovel')),
            ],
            options={
                'verbose_name': 'Contato',
                'verbose_name_plural': 'Contatos',
                'ordering': ['-data'],
            },
        ),
        migrations.AddField(
            model_name='imovel',
            name='proprietario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='imoveis', to='Imob.proprietario'),
        ),
        migrations.CreateModel(
            name='ImovelComodidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comodidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Imob.comodidade')),
                ('imovel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comodidades', to='Imob.imovel')),
            ],
            options={
                'verbose_name': 'Comodidade do Imóvel',
                'verbose_name_plural': 'Comodidades do Imóvel',
                'unique_together': {('imovel', 'comodidade')},
            },
        ),
    ]
