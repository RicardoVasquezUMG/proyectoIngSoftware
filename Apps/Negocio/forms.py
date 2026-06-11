from django import forms

from Apps.Cliente.models import Producto

from .models import Oferta


class OfertaForm(forms.ModelForm):
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all().order_by('nombre'),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Productos'
    )

    class Meta:
        model = Oferta
        fields = ['inicio', 'fin', 'estado', 'descuento', 'productos']
        widgets = {
            'inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['productos'].initial = self.instance.productos.all()