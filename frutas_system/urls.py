from django.contrib import admin
from app_frutas_sys import views
from django.urls import path
from app_frutas_sys.views import download_pedido



urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('criar-pedido/', views.criar_pedido, name='criar_pedido'),  # Atualização feita aqui
    path('formulario_criar_pedido/', views.formulario_criar_pedido, name='formulario_criar_pedido'),
    path('ver_pedidos/<int:pedido_id>/', views.ver_pedido_detalhes, name='ver_pedido'),
    path('admin/', admin.site.urls),
    path('concluir_pedido/<int:pedido_id>/', views.concluir_pedido, name='concluir_pedido'),
    
    path('download_pedido/<int:pedido_id>/', download_pedido, name='download_pedido'),
    path('apagar_pedido/<int:pedido_id>/', views.apagar_pedido, name='apagar_pedido'),
    path('concluir_pedido/', views.concluir_pedido, name='concluir_pedido'),
    path('sucesso/', views.sucesso, name='sucesso'),
    
    path('pedido/modificar/<int:pedido_id>/', views.modificar_pedido, name='modificar_pedido'),
    path('pedido/adicionar_item/<int:pedido_id>/', views.adicionar_item_pedido, name='adicionar_item_pedido'),
    path('pedido/remover_item/<int:pedido_id>/<int:item_id>/', views.remover_item_pedido, name='remover_item_pedido'),
    path('adicionar_pedido_dashboard/<int:pedido_id>/', views.adicionar_pedido_dashboard, name='adicionar_pedido_dashboard')   
]
