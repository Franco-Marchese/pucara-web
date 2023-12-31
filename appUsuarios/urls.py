from django.contrib import admin
from django.urls import path, include
from .views import IngresoView, EgresoView, RegistrarView, UsuariosView, EliminarView

urlpatterns = [
    path("", IngresoView.as_view(), name='ingreso'),
    path("egreso/", EgresoView.as_view(), name='egreso'),
    path("registrar/", RegistrarView.as_view(), name='registrar'),
    path("usuarios/", UsuariosView.as_view(), name='usuarios'),
    path("eliminar/<int:id>", EliminarView.as_view(), name='eliminar'),
]