from django import forms
from .models import Mesa
from django.forms import NumberInput

class VotoForm(forms.Form):
    num_orden = forms.IntegerField(label='Número de Orden',widget=forms.NumberInput(attrs={'class': 'form-control'}))

class NumeroMesaForm(forms.Form):
    mesa_choices = [(mesa.num_mesa, f'Mesa {mesa.num_mesa}') for mesa in Mesa.objects.all()]
    numero_mesa = forms.ChoiceField(label='Número de Mesa', choices=mesa_choices, widget=forms.Select(attrs={'class': 'form-control'}))