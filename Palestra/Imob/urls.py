from django.urls import path
from . import views

urlpatterns = [
    # Página inicial
    path('', views.lista_imoveis, name='lista_imoveis'),

    # Detalhes de um imóvel específico
    path('imovel/<int:pk>/', views.detalhes_imovel, name='detalhes_imovel'),
]