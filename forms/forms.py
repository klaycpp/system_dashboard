from django import forms
from app_frutas_sys.models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['data_pedido', 'status']
        widgets = {
            'data_pedido': forms.DateInput(attrs={'type': 'date'}),
        }
