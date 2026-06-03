from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from Apps.Cliente.views import DetalleProductoView, ListadoView, LoginView, RegistroView, CarritoView
from Apps.Cliente.views import agregar_al_carrito, quitar_del_carrito


app_name = 'Cliente'
urlpatterns = [
    path('login/', LoginView.as_view(), name='loginapp'),
    path('logout/', LogoutView.as_view(next_page='Home:homeapp'), name='logout'),
    path('registrar/', RegistroView.as_view(), name='registrarCliente'),
    path('listado/', ListadoView.as_view(), name='listadoProductos'),
    path('producto/<int:producto_id>/', DetalleProductoView.as_view(), name='detalle_producto'),
    path('carrito/', CarritoView.as_view(), name='carrito'),
    path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='carrito_agregar'),
    path('carrito/quitar/<int:producto_id>/', quitar_del_carrito, name='carrito_quitar'),
]
