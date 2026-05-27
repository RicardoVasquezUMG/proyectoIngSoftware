from django.contrib import admin
from django.urls import include, path
from .views import CategoriaCRUDView, CategoriaCrearView, CategoriaEditarView, CategoriaEliminarView
from .views import ProductoCRUDView, ProductoCrearView, ProductoEditarView, ProductoEliminarView, ProductoView

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
]
