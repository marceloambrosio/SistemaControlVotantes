from django import forms

class VotoForm(forms.Form):
    num_orden = forms.IntegerField(label='Número de Orden')