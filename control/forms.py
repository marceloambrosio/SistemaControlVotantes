from django import forms
from django.forms import NumberInput

class VotoForm(forms.Form):
    num_orden = forms.IntegerField(label='Número de Orden',widget=forms.NumberInput(attrs={'class': 'form-control'}))

class NumeroMesaForm(forms.Form):
    numero_mesa = forms.IntegerField(label='Número de Mesa',widget=forms.NumberInput(attrs={'class': 'form-control'}))