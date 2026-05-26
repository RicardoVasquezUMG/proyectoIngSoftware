from django.contrib import admin
from django.urls import include, path
from .views import CategoriaCRUDView, CategoriaCrearView, CategoriaEditarView, CategoriaEliminarView


app_name = 'Negocio'
urlpatterns = [
    path('CRUDcategoria/', CategoriaCRUDView.as_view(), name='categoria_crud'),
    path('CRUDcategoria/crear/', CategoriaCrearView.as_view(), name='categoria_crear'),
    path('CRUDcategoria/<int:pk>/editar/', CategoriaEditarView.as_view(), name='categoria_editar'),
    path('CRUDcategoria/<int:pk>/eliminar/', CategoriaEliminarView.as_view(), name='categoria_eliminar'),
]
