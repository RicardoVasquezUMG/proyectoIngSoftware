from django.contrib import admin
from django.urls import include, path
from .views import CategoriaCRUDView, CategoriaCrearView, CategoriaEditarView, CategoriaEliminarView, PedidoEliminarView
from .views import ProductoCRUDView, ProductoCrearView, ProductoEditarView, ProductoEliminarView, ProductoView
from .views import PedidoCRUDView, PedidoEditarView, PedidoView



app_name = 'Negocio'
urlpatterns = [
    path('CRUDcategoria/', CategoriaCRUDView.as_view(), name='categoria_crud'),
    path('CRUDcategoria/crear/', CategoriaCrearView.as_view(), name='categoria_crear'),
    path('CRUDcategoria/<int:pk>/editar/', CategoriaEditarView.as_view(), name='categoria_editar'),
    path('CRUDcategoria/<int:pk>/eliminar/', CategoriaEliminarView.as_view(), name='categoria_eliminar'),
    path('CRUDproducto/', ProductoCRUDView.as_view(), name='producto_crud'),
    path('CRUDproducto/<int:pk>/editar/', ProductoEditarView.as_view(), name='producto_editar'),
    path('CRUDproducto/crear/', ProductoCrearView.as_view(), name='producto_crear'),
    path('CRUDproducto/<int:pk>/', ProductoView.as_view(), name='producto_ver'),
    path('CRUDproducto/<int:pk>/eliminar/', ProductoEliminarView.as_view(), name='producto_eliminar'),
    path('CRUDpedido/', PedidoCRUDView.as_view(), name='pedido_crud'),
    path('CRUDpedido/<int:pk>/', PedidoView.as_view(), name='pedido_ver'),
    path('CRUDpedido/<int:pk>/editar/', PedidoEditarView.as_view(), name='pedido_editar'),
    path('CRUDpedido/<int:pk>/eliminar/', PedidoEliminarView.as_view(), name='pedido_eliminar'),
]
