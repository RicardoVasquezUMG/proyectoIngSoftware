from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404, redirect
from   Apps.Cliente.models import Categoria , Producto
from Apps.Cliente.forms import CategoriaForm, ProductoForm

# Create your views here.
class CategoriaCRUDView(TemplateView):
    template_name = 'categoria_crud.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context
    

class CategoriaCrearView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoriaCrear.html'
    success_url = reverse_lazy('Negocio:categoria_crud')

class CategoriaEditarView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoriaEditar.html'
    success_url = reverse_lazy('Negocio:categoria_crud')

class CategoriaEliminarView(View):
    def post(self, request, pk, *args, **kwargs):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return redirect('Negocio:categoria_crud')
    


class ProductoCRUDView(TemplateView):
    template_name = 'producto_crud.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        categoria_id = request.GET.get('categoria')
        if categoria_id:
            productos = Producto.objects.filter(categoria_id=categoria_id)
        else:
            productos = Producto.objects.all()
        context['productos'] = productos
        context['categorias'] = Categoria.objects.all()
        return context

class ProductoView(TemplateView):
    template_name = 'productoVer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto_id = self.kwargs.get('pk')
        try:
            producto = Producto.objects.get(id=producto_id)
            context['producto'] = producto
        except Producto.DoesNotExist:
            context['error_message'] = 'Producto no encontrado.'
        return context

class ProductoEditarView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productoEditar.html'
    success_url = reverse_lazy('Negocio:producto_crud')


class ProductoCrearView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productoCrear.html'
    success_url = reverse_lazy('Negocio:producto_crud')

class ProductoEliminarView(View):
    def post(self, request, pk, *args, **kwargs):
        producto = get_object_or_404(Producto, pk=pk)
        producto.delete()
        return redirect('Negocio:producto_crud')   
    
