from django.db import models

# Create your models here.

class Usuario(models.Model):
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, default="")
    nombre = models.CharField(max_length=255)
    equipo = models.CharField(max_length=255)
    es_admin = models.CharField(max_length=255)