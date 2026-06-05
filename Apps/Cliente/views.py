from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from .forms import ClienteForm, ClienteUpdateForm
from django.contrib.auth.models import User
from django.db import transaction
from .models import Categoria, Cliente, Producto
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Direccion
from .forms import DireccionForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from Apps.Negocio.models import Pedido, PedidoDetalle

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
	

@require_POST
def agregar_al_carrito(request, producto_id):
	producto = Producto.objects.get(id=producto_id)
	carrito = request.session.get('carrito', {})
	cantidad = int(request.POST.get('cantidad', 1))
	if cantidad <= 0:
		return redirect('Cliente:carrito')
	if str(producto_id) in carrito:
		carrito[str(producto_id)]['cantidad'] += cantidad
	else:
		carrito[str(producto_id)] = {
			'id': producto.id,
			'nombre': producto.nombre,
			'precio': float(producto.precio),
			'cantidad': cantidad,
			'imagen': producto.imagen,
			'color': getattr(producto, 'color', ''),
			'size': getattr(producto, 'size', '')
		}
	# Actualizar la cantidad total de productos en el carrito
	carrito_cantidad = sum(item['cantidad'] for item in carrito.values())
	request.session['carrito'] = carrito
	request.session['carrito_cantidad'] = carrito_cantidad
	request.session.modified = True
	return redirect('Cliente:carrito')

@require_POST
def quitar_del_carrito(request, producto_id):
	carrito = request.session.get('carrito', {})
	producto_key = str(producto_id)
	if producto_key in carrito:
		if request.POST.get('delete') == '1':
			carrito.pop(producto_key, None)
		else:
			nueva_cantidad = int(request.POST.get('cantidad', carrito[producto_key]['cantidad'] - 1))
			if nueva_cantidad <= 0:
				carrito.pop(producto_key, None)
			else:
				carrito[producto_key]['cantidad'] = nueva_cantidad
	# Actualizar la cantidad total de productos en el carrito
	carrito_cantidad = sum(item['cantidad'] for item in carrito.values())
	request.session['carrito'] = carrito
	request.session['carrito_cantidad'] = carrito_cantidad
	request.session.modified = True
	return redirect('Cliente:carrito')


class PerfilView(TemplateView):
	template_name = 'perfil.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			cliente = Cliente.objects.get(perfil=self.request.user)
			context['cliente'] = cliente
		except Cliente.DoesNotExist:
			context['error_message'] = "No se encontró al usuario."
		return context
	
class EditarPerfilView(UpdateView):
	model = User
	form_class = ClienteUpdateForm
	template_name = 'editar_perfil.html'
	success_url = reverse_lazy('Cliente:perfil')

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_object(self, queryset=None):
		return self.request.user

	def form_valid(self, form):
		# Guardar User y Cliente en una transacción atómica
		with transaction.atomic():
			response = super().form_valid(form)
		messages.success(self.request, "Perfil actualizado correctamente.")
		return response

class DireccionesCRUDView(TemplateView):
	template_name = 'direccionesCRUD.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			cliente = Cliente.objects.get(perfil=self.request.user)
			context['cliente'] = cliente
			context['direcciones'] = Direccion.objects.filter(cliente=cliente)
		except Cliente.DoesNotExist:
			context['error_message'] = "No se encontró el cliente asociado al usuario."
		return context
	

class CrearDireccionView(CreateView):
	# Implementación para crear una nueva dirección
	model = Direccion
	form_class = DireccionForm
	template_name = 'direccionesCrear.html'
	success_url = reverse_lazy('Cliente:direcciones')

	def form_valid(self, form):
		direccion = form.save(commit=False)
		try:
			cliente = Cliente.objects.get(perfil=self.request.user)
			direccion.cliente = cliente
		except Cliente.DoesNotExist:
			messages.error(self.request, "No se encontró el cliente asociado al usuario.")
			return redirect('Cliente:loginapp')
		direccion.save()
		messages.success(self.request, "Dirección creada exitosamente.")
		return redirect(self.success_url)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			cliente = Cliente.objects.get(perfil=self.request.user)
			context['cliente'] = cliente
		except Cliente.DoesNotExist:
			context['cliente'] = None
		return context
	
# Vista para editar dirección
class EditarDireccionView(UpdateView):
		model = Direccion
		form_class = DireccionForm
		template_name = 'editar_direccion.html'
		success_url = reverse_lazy('Cliente:direcciones')

		def get_context_data(self, **kwargs):
			context = super().get_context_data(**kwargs)
			try:
				cliente = Cliente.objects.get(perfil=self.request.user)
				context['cliente'] = cliente
			except Cliente.DoesNotExist:
				context['cliente'] = None
			return context

		def form_valid(self, form):
			direccion = form.save(commit=False)
			try:
				cliente = Cliente.objects.get(perfil=self.request.user)
				direccion.cliente = cliente
			except Cliente.DoesNotExist:
				messages.error(self.request, "No se encontró el cliente asociado al usuario.")
				return redirect('Cliente:loginapp')
			direccion.save()
			messages.success(self.request, "Dirección editada exitosamente.")
			return redirect(self.success_url)

# Vista para eliminar dirección
class EliminarDireccionView(DeleteView):
	model = Direccion
	template_name = 'eliminar_direccion.html'
	success_url = reverse_lazy('Cliente:direcciones')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			cliente = Cliente.objects.get(perfil=self.request.user)
			context['cliente'] = cliente
		except Cliente.DoesNotExist:
			context['cliente'] = None
		return context

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, "Dirección eliminada exitosamente.")
		return super().delete(request, *args, **kwargs)
	

@login_required
def formulario_pedido(request):
	cliente = Cliente.objects.get(perfil=request.user)
	direcciones = Direccion.objects.filter(cliente=cliente)
	carrito = request.session.get('carrito', {})
	productos = []
	total = 0
	for key, item in carrito.items():
		subtotal = item['precio'] * item['cantidad']
		total += subtotal
		productos.append(item)

	if request.method == 'POST':
		retiro_tienda = request.POST.get('retiro_tienda') == 'true'
		direccion_id = request.POST.get('direccion') if not retiro_tienda else None
		comentario = request.POST.get('comentario', '')
		direccion_obj = Direccion.objects.get(id=direccion_id) if direccion_id else None
		pedido = Pedido.objects.create(
			cliente=cliente,
			envio=not retiro_tienda,
			estado='pendiente',
			direccion_envio=direccion_obj,
			comentarios=comentario
		)
		for item in productos:
			producto_obj = Producto.objects.get(id=item['id'])
			PedidoDetalle.objects.create(
				pedido=pedido,
				producto=producto_obj,
				cantidad=item['cantidad']
			)
		# Limpiar carrito
		request.session['carrito'] = {}
		request.session['carrito_cantidad'] = 0
		request.session.modified = True
		return redirect(reverse('Cliente:ordenes_ver', args=[pedido.id]))

	return render(request, 'pedido_formulario.html', {
		'direcciones': direcciones,
		'productos': productos,
		'total': total
	})

	

class OrdenesVerView(TemplateView):
	template_name = 'ordenesVer.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pedido_id = self.kwargs.get('pedido_id')
		try:
			pedido = Pedido.objects.get(id=pedido_id)
			detalles = PedidoDetalle.objects.filter(pedido=pedido)
			subtotal = sum(float(d.producto.precio) * d.cantidad for d in detalles)
			if pedido.envio:
				envio = 0 if subtotal > 75 else 25
			else:
				envio = 0
			total = subtotal + envio
			context['pedido'] = pedido
			context['detalles'] = detalles
			context['cliente'] = pedido.cliente
			context['subtotal'] = subtotal
			context['envio'] = envio
			context['total'] = total
		except Pedido.DoesNotExist:
			context['error_message'] = 'Pedido no encontrado.'
		return context