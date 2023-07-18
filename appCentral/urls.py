from django.urls import path, include
from django.contrib import admin
from .views import MenuView, VerRegistrosView, NuevoRegistroView


urlpatterns = [
    path("menu/", MenuView.as_view(), name='menu'),
    path("registros/", VerRegistrosView.as_view(), name='registros'),
    path("registros/nuevo/", NuevoRegistroView.as_view(), name='nuevoRegistro'),
]