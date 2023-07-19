from django.utils.decorators import method_decorator
from appUsuarios.utils import token_requerido, firmar
from .models import Conductor, Camion, Registro
from appUsuarios.models import Usuario
from django.shortcuts import render, redirect
from django.views import View
import pandas as pd

# Create your views here.
class MenuView(View):
    @method_decorator(token_requerido)
    def get(self, request):
        _id = firmar(request)
        usuario = Usuario.objects.get(id=_id)
        # Retorna todas las opciones disponibles según el usuario.
        # FALTRA FILTRAR LAS ACCIONES DISPONIBLES.  
        return render(request, "menu.html", {
            "nombre":usuario.nombre,
        })

class VerRegistrosView(View):
    registros = Registro.objects.all()
    # reg = registros.first()

    @method_decorator(token_requerido)
    def get(self, request):
        _id = firmar(request)
        usuario = Usuario.objects.get(id=_id)
        # cabecillas = len(self.reg_meta.fields)


        return render(request, 'registros.html', {
            "nombre":usuario.nombre,
            "registros":self.registros,
        })
    
    @method_decorator(token_requerido)
    def post(self, request):
        pass

class NuevoRegistroView(View):
    @method_decorator(token_requerido)
    def get(self, request):
        # Junta algunos de los datos necesarios para completar el formulario.
        conductores = Conductor.objects.all()
        camiones = Camion.objects.all()
        # Obtiene al autor del formulario por completaren base a la sesión iniciada.
        firmado = firmar(request=request)
        autor = Usuario.objects.get(id=firmado)
        return render(request, 'nuevoRegistro.html', {
            "conductores":conductores,
            "camiones":camiones,
            "autor":autor,
        })
    
    @method_decorator(token_requerido)
    def post(self, request):
        # Obtiene al autor del formulario por completaren base a la sesión iniciada.
        firmado = firmar(request=request)
        autor = Usuario.objects.get(id=firmado)
        # Captura los valores sencillos del formulario.
        tracto = request.POST["tracto"]
        cargado = request.POST.get("cargado", 0)
        ppu = request.POST["ppu"]
        sello = request.POST["sello"]
        # Captura y procesa los valores complejos del formulario
        baseFecha = request.POST["fecha"] # -> Pieza completa.
        fecha = baseFecha.split("T")[0] # -> Separación.
        hora = baseFecha.split("T")[1] # -> Separación.
        contIni = request.POST["comienzoContenedor"] # -> Parte por unir.
        contFin = request.POST["finalContenedor"] # -> Parte por unir.
        contenedor = "{}-{}".format(contIni, contFin) # -> Pieza completa.
        # Obtiene los otros registros relacionados del formulario y firma.
        idConductor = Conductor.objects.get(id=request.POST["idConductor"])
        idCamion = Camion.objects.get(id=request.POST["idCamion"])
        idUsuario = Usuario.objects.get(id=autor)
        # Instancia el nuevo registro.
        nuevoRegistro = Registro.objects.create(
            tracto=tracto,
            cargado=int(cargado),
            hora=hora,
            fecha=fecha,
            ppu=ppu,
            contenedor=contenedor,
            sello=sello,
            idConductor=idConductor,
            idCamion=idCamion,
            idUsuario=idUsuario,
        )
        # Guarda el nuevo registro.
        nuevoRegistro.save()
        return redirect("registros")
