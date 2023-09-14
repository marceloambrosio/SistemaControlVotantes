from django import forms
from .models import Mesa
from django.forms import NumberInput

class VotoForm(forms.Form):
    num_orden = forms.IntegerField(label='Número de Orden',widget=forms.NumberInput(attrs={'class': 'form-control'}))

class NumeroMesaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        mesas = kwargs.pop('mesas', None)
        super(NumeroMesaForm, self).__init__(*args, **kwargs)
        
        if mesas:
            self.fields['numero_mesa'].choices = [(mesa.num_mesa, f'Mesa {mesa.num_mesa}') for mesa in mesas]

    numero_mesa = forms.ChoiceField(label='Número de Mesa', widget=forms.Select(attrs={'class': 'form-control'}))
