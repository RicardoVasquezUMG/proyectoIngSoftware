from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Categoria, Cliente, Direccion, Producto


class ClienteForm(UserCreationForm):
    nombre = forms.CharField(max_length=30, required=True, label='Nombre')
    apellido = forms.CharField(max_length=140, required=True, label='Apellido')
    telefono = forms.CharField(max_length=20, required=True, label='Teléfono')
    email = forms.EmailField(required=True, label='Correo Electrónico')

    class Meta:
        model = User
        fields = ['nombre', 'apellido', 'telefono', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellido']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            Cliente.objects.update_or_create(perfil=user, defaults={'telefono': self.cleaned_data['telefono']})
        return user

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto        
        exclude = ['creacion'] 

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        exclude = ['cliente']
        widgets = {
            'direccion_linea1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección principal'}),
            'direccion_linea2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección secundaria (opcional)'}),
            'Colonia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Colonia'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'etiqueta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Etiqueta (ej. Casa, Oficina)'}),
            'entrega': forms.Select(attrs={'class': 'form-control'}),
        }


class ClienteUpdateForm(forms.ModelForm):
    telefono = forms.CharField(max_length=20, required=False, label='Teléfono')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar el campo telefono desde el modelo Cliente si existe
        user = kwargs.get('instance')
        if user is not None:
            try:
                cliente = user.cliente
                self.fields['telefono'].initial = cliente.telefono
            except Exception:
                pass

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email

        if commit:
            user.save()

        telefono = self.cleaned_data.get('telefono', '')
        Cliente.objects.update_or_create(perfil=user, defaults={'telefono': telefono})
        return user