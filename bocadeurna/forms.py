from django import forms
from .models import DetalleBocaDeUrna, Candidato

class DetalleBocaDeUrnaForm(forms.ModelForm):
    class Meta:
        model = DetalleBocaDeUrna
        fields = ['edad', 'candidato']
        widgets = {
            'circuito': forms.HiddenInput(),  # Ocultamos el campo circuito
        }

    def __init__(self, *args, circuito_usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.circuito_usuario = circuito_usuario
        # Agregamos un queryset para obtener solo los candidatos del circuito del usuario
        if self.circuito_usuario:
            candidatos_del_circuito = Candidato.objects.filter(circuito=self.circuito_usuario)
            self.fields['candidato'].queryset = candidatos_del_circuito
            self.fields['candidato'].label_from_instance = lambda obj: f"{obj.nombre} {obj.apellido}"