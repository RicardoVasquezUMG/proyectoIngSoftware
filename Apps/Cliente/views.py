from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from .forms import ClienteForm
from .models import Cliente

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
