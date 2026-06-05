from django.db import models

# Create your models here.
class Pedido(models.Model):
    cliente = models.ForeignKey('Cliente.Cliente', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    envio = models.BooleanField(default=False)
    estado = models.CharField(max_length=50)
    direccion_envio = models.ForeignKey('Cliente.Direccion', on_delete=models.SET_NULL, null=True, blank=True)
    comentarios = models.TextField(blank=True)
    
    def __str__(self):
        return f'Pedido {self.id} - Cliente: {self.cliente.perfil.username} - Envío: {self.envio} - Dirección: {self.direccion_envio}'
    

class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey('Cliente.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    