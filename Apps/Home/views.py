from django.shortcuts import render
from django.views.generic import TemplateView

from Apps.Cliente.models import Producto

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class AcercaView(TemplateView): 
    template_name = 'acerca.html'

class SoporteView(TemplateView):
    template_name = 'soporte.html' 


class SearchResultsView(TemplateView):
    template_name = 'search-results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vNombre=self.request.GET.get('dato')
        if vNombre:
            context['results'] = Producto.objects.filter(nombre__icontains=vNombre)
        else:
            context['results'] = Producto.objects.all()
        return context