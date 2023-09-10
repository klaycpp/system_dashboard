from django.contrib import admin
from .models import Pedido, ItemPedido

class ItemPedidoInline(admin.TabularInline):  # Utilize TabularInline para exibir os itens de pedido de forma tabular
    model = ItemPedido
    extra = 1  # Define quantos itens de pedido em branco são exibidos por padrão

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_pedido', 'status')
    inlines = [ItemPedidoInline]  # Adiciona a classe Inline para mostrar os itens do pedido dentro do painel do pedido

class PedidoDashboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_sequencial', 'nome_pedido', 'pedido')

# Registrar os modelos com as classes de admin personalizadas
admin.site.register(Pedido, PedidoAdmin)

