from django.db import models
from appUsuarios.models import Usuario

# Create your models here.
class Conductor(models.Model):
    nombre = models.CharField(blank=False, default=None, max_length=255)
    email = models.EmailField(blank=True, default=None, unique=True)
    telefono = models.CharField(blank=False, default=None, max_length=255)

class Camion(models.Model):
    nombre = models.CharField(blank=False, default=None, max_length=255)
    patente = models.CharField(blank=False, default=None, max_length=255)

class Registro(models.Model):
    tracto = models.IntegerField(blank=False, default=None)
    cargado = models.BooleanField(blank=False, default=None)
    hora = models.CharField(blank=False, default=None, max_length=255)
    fecha = models.CharField(blank=False, default=None, max_length=255)
    ppu = models.CharField(blank=False, default=None, max_length=255)
    contenedor = models.CharField(blank=False, default=None, max_length=255)
    sello = models.CharField(blank=False, default=None, max_length=255)

    idConductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    idCamion = models.ForeignKey(Camion, on_delete=models.CASCADE)
