from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from Apps.Cliente.views import LoginView, RegistroView

app_name = 'Cliente'
urlpatterns = [
    path('login/', LoginView.as_view(), name='loginapp'),
    path('logout/', LogoutView.as_view(next_page='Home:homeapp'), name='logout'),
    path('registrar/', RegistroView.as_view(), name='registrarCliente'),
]
