from django.contrib import admin
from .models import Categoria, Cliente

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Categoria)