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
]