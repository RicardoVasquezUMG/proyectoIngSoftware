from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cliente(models.Model):
    perfil = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.perfil.username
    
