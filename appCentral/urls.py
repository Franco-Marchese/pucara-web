from django.urls import path, include
from django.contrib import admin
from .views import VerRegistrosView, NuevoRegistroView, PoblandoView


urlpatterns = [
    path("registros/", VerRegistrosView.as_view(), name='registros'),
    path("registros/nuevo/", NuevoRegistroView.as_view(), name='nuevoRegistro'),

    path("poblando/", PoblandoView.as_view(), name='poblando'),
]