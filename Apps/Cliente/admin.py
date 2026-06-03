from django.contrib import admin
from .models import Categoria, Cliente, Direccion, Producto

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Direccion)
    