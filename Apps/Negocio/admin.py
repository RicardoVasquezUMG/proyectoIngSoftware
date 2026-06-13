from django.contrib import admin
from .models import Oferta, ProductoOferta, Pedido, PedidoDetalle


admin.site.register(Oferta)
admin.site.register(ProductoOferta)
admin.site.register(Pedido)
admin.site.register(PedidoDetalle)
