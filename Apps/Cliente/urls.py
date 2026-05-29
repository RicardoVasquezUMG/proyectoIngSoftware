from django.urls import include, path
from django.contrib import admin

from Apps.Cliente.views import LoginView, RegistroView

app_name = 'Cliente'
urlpatterns = [
    path('login/', LoginView.as_view(), name='loginapp'),
    path('registrar/', RegistroView.as_view(), name='registrarCliente'),
]
