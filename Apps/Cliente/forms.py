from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Categoria, Cliente


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