from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cliente(models.Model):
    perfil = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.perfil.username
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.CharField(max_length=1000)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, default=1)  # Assuming 'General' has ID 1 in Categoria

    def __str__(self):
        return self.nombre  