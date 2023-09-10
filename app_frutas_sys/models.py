from django.db import models
from django import forms
from django.utils import timezone  # Importe o timezone do Django

class Pedido(models.Model):
    status = models.CharField(max_length=50, default='Pendente')
    data_pedido = models.DateField(default=timezone.now)  # Use timezone.now() para definir a data padrão

    def __str__(self):
        return f"Pedido #{self.id}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return f"Item do Pedido #{self.pedido.id}"

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['data_pedido']
        
        
