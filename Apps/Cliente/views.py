from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from .forms import ClienteForm
from .models import Categoria, Cliente, Producto

# Create your views here.
class RegistroView(CreateView):
    template_name = 'register.html'
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('Cliente:loginapp')

class LoginView(LoginView):
	template_name = 'login.html'
	success_url = reverse_lazy('Home:homeapp')

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form, error_message="Usuario o contraseña incorrectos."))


class ListadoView(TemplateView):
	template_name = 'listadoProductos.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		categoria_id = self.request.GET.get('categoria')
		if categoria_id:
			context['productos'] = Producto.objects.filter(categoria_id=categoria_id)
		else:
			context['productos'] = Producto.objects.all()
		context['categorias'] = Categoria.objects.all()
		return context
	
class DetalleProductoView(TemplateView):
	template_name = 'detalle_producto.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		producto_id = self.kwargs.get('producto_id')
		try:
			producto = Producto.objects.get(id=producto_id)
			context['producto'] = producto
		except Producto.DoesNotExist:
			context['error_message'] = 'Producto no encontrado.'
		return context
	

class CarritoView(TemplateView):
	template_name = 'carrito.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		carrito = self.request.session.get('carrito', {})
		productos = []
		total = 0
		for key, item in carrito.items():
			producto_id = item.get('id') or key
			subtotal = item['precio'] * item['cantidad']
			total += subtotal
			productos.append({
				'id': producto_id,
				'nombre': item['nombre'],
				'precio': item['precio'],
				'cantidad': item['cantidad'],
				'imagen': item.get('imagen', ''),
				'subtotal': subtotal
			})
		context['productos'] = productos
		context['total'] = total
		return context