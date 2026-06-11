from django.db import models

# Create your models here.
class Oferta(models.Model):
    ESTADO_ACTIVA = 'activa'
    ESTADO_INACTIVA = 'inactiva'

    ESTADO_CHOICES = [
        (ESTADO_ACTIVA, 'Activa'),
        (ESTADO_INACTIVA, 'Inactiva'),
    ]

    inicio = models.DateField()
    fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_ACTIVA)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    productos = models.ManyToManyField('Cliente.Producto', through='ProductoOferta', related_name='ofertas', blank=True)

    def __str__(self):
        return f'Oferta {self.id} - {self.descuento}%'


class ProductoOferta(models.Model):
    producto = models.ForeignKey('Cliente.Producto', on_delete=models.CASCADE)
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('producto', 'oferta')

    def __str__(self):
        return f'{self.producto} -> {self.oferta}'


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
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    