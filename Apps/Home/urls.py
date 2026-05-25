from django.contrib import admin
from django.urls import include, path
from Apps.Home.views import AcercaView, HomeView, SoporteView

app_name = 'Home'
urlpatterns = [
    path('', HomeView.as_view(), name='homeapp'),
    path('acerca/', AcercaView.as_view(), name='acerca_app'),
    path('soporte/', SoporteView.as_view(), name='soporte_app'),
]
