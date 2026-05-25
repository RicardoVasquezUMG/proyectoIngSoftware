from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class AcercaView(TemplateView): 
    template_name = 'acerca.html'

class SoporteView(TemplateView):
    template_name = 'soporte.html' 