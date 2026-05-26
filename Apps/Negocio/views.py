from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404, redirect
from   Apps.Cliente.models import Categoria
from Apps.Cliente.forms import CategoriaForm

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