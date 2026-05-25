from django.contrib import admin
from django.urls import include, path
from Apps.Home.views import HomeView

app_name = 'Home'
urlpatterns = [
    path('', HomeView.as_view(), name='homeapp'),
]
