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
    
class Direccion(models.Model):
    entrega_CHOICES = [
        ('Encontrarse', 'Encontrarse'),
        ('Dejar en puerta', 'Dejar en puerta'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    direccion_linea1 = models.CharField(max_length=255)
    direccion_linea2 = models.CharField(max_length=255, blank=True, null=True)
    Colonia = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    etiqueta = models.CharField(max_length=50, blank=True, null=True)
    entrega = models.CharField(max_length=50, choices=entrega_CHOICES, default='Encontrarse')

    def __str__(self):
        return f"{self.direccion_linea1}, {self.Colonia}, {self.telefono}"