from django.urls import path
from . import views

urlpatterns = [
    # URLs públicas
    path('', views.home, name='home'),
    path('imovel/<int:imovel_id>/', views.detalhes_imovel, name='detalhes_imovel'),
    path('imovel/', views.lista_imoveis, name='lista_imoveis'),
    
    # URLs de autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # URLs protegidas (admin)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('imovel/cadastrar/', views.cadastrar_imovel, name='cadastrar_imovel'),
    path('imovel/<int:imovel_id>/editar/', views.editar_imovel, name='editar_imovel'),
    
    path('imovel/<int:imovel_id>/excluir/', views.excluir_imovel, name='excluir_imovel'),
    path('proprietarios/cadastrar/', views.cadastrar_proprietario, name='cadastrar_proprietario'),
    path('proprietarios/', views.listar_proprietarios, name='listar_proprietarios'),
    path('proprietarios/<int:id>/editar/', views.editar_proprietario, name='editar_proprietario'),
    path('proprietarios/<int:id>/visualizar/', views.visualizar_proprietario, name='visualizar_proprietario'),
    path('proprietarios/<int:id>/excluir/', views.excluir_proprietario, name='excluir_proprietario'),
    path('imovel/<int:imovel_id>/fotos/', views.upload_fotos_imovel, name='upload_fotos_imovel'),
    path('imovel/upload_ajax/', views.upload_foto_ajax, name='upload_foto_ajax'),
]