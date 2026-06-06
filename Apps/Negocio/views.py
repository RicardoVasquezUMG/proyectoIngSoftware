from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404, redirect
from Apps.Cliente.models import Categoria , Producto
from Apps.Cliente.forms import CategoriaForm, ProductoForm
from .models import Pedido, PedidoDetalle
from django.forms import modelformset_factory
from django import forms


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
    


class PedidoCRUDView(TemplateView):
    template_name = 'pedidoCRUD.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Pedido
        context['pedidos'] = Pedido.objects.all()
        return context


# Ver pedido
class PedidoView(TemplateView):
    template_name = 'pedidoVer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedido_id = self.kwargs.get('pk')
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        detalles = PedidoDetalle.objects.filter(pedido=pedido)
        subtotal = sum(float(d.producto.precio) * d.cantidad for d in detalles)
        if pedido.envio:
            envio = 0 if subtotal > 75 else 25
        else:
            envio = 0
        total = subtotal + envio
        context['pedido'] = pedido
        context['detalles'] = detalles
        context['subtotal'] = subtotal
        context['envio'] = envio
        context['total'] = total
        context['cliente'] = pedido.cliente
        return context

# Editar pedido

# Formulario solo para el campo estado
class PedidoEstadoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']

class PedidoDetalleCantidadForm(forms.ModelForm):
    class Meta:
        model = PedidoDetalle
        fields = ['cantidad']

class PedidoEditarView(View):
    template_name = 'pedidoEditar.html'
    success_url = reverse_lazy('Negocio:pedido_crud')

    def get(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        estado_form = PedidoEstadoForm(instance=pedido)
        DetalleFormSet = modelformset_factory(PedidoDetalle, form=PedidoDetalleCantidadForm, extra=0)
        detalles = PedidoDetalle.objects.filter(pedido=pedido)
        detalle_formset = DetalleFormSet(queryset=detalles)
        return render(request, self.template_name, {
            'estado_form': estado_form,
            'detalle_formset': detalle_formset,
            'pedido': pedido
        })

    def post(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        estado_form = PedidoEstadoForm(request.POST, instance=pedido)
        DetalleFormSet = modelformset_factory(PedidoDetalle, form=PedidoDetalleCantidadForm, extra=0)
        detalles = PedidoDetalle.objects.filter(pedido=pedido)
        detalle_formset = DetalleFormSet(request.POST, queryset=detalles)
        if estado_form.is_valid() and detalle_formset.is_valid():
            estado_form.save()
            detalle_formset.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {
            'estado_form': estado_form,
            'detalle_formset': detalle_formset,
            'pedido': pedido
        })


# Eliminar pedido
class PedidoEliminarView(View):
    def post(self, request, pk, *args, **kwargs):
        pedido = get_object_or_404(Pedido, pk=pk)
        pedido.delete()
        return redirect('Negocio:pedido_crud')