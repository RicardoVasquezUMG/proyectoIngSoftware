from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from Apps.Cliente.views import DetalleProductoView, ListadoView, LoginView, RegistroView, CarritoView
from Apps.Cliente.views import agregar_al_carrito, quitar_del_carrito
from Apps.Cliente.views import PerfilView, DireccionesCRUDView, CrearDireccionView, EditarDireccionView, EliminarDireccionView
from Apps.Cliente.views import EditarPerfilView


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
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('perfil/editar/', EditarPerfilView.as_view(), name='editar_perfil'),
    path('direcciones/', DireccionesCRUDView.as_view(), name='direcciones'),
    path('direcciones/crear/', CrearDireccionView.as_view(), name='crear_direccion'),
    path('direcciones/<int:pk>/editar/', EditarDireccionView.as_view(), name='editar_direccion'),
    path('direcciones/<int:pk>/eliminar/', EliminarDireccionView.as_view(), name='eliminar_direccion'),
]
