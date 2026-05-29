from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy

# Create your views here.
class LoginView(TemplateView):
	template_name = 'login.html'
	
class RegistroView(TemplateView):
    template_name = 'register.html'