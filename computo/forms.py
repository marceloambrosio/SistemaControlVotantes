from django import forms

class VotosForm(forms.Form):
    def __init__(self, *args, **kwargs):
        detalles = kwargs.pop('detalles')  # Cambiar 'detalle' a 'detalles' aquí
        super(VotosForm, self).__init__(*args, **kwargs)
        for detalle in detalles:  # Cambiar 'candidato' a 'detalle' aquí
            self.fields[f'votos_{detalle.candidato_eleccion.candidato.id}'] = forms.IntegerField(
                initial=detalle.cantidad_voto,
                label=f'Votos para {detalle.candidato_eleccion.candidato.nombre} {detalle.candidato_eleccion.candidato.apellido}'
            )
