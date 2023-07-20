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
            "nombre":usuario.nombre,})
        

class VerRegistrosView(View):
    registros = Registro.objects.all()
    # reg = registros.first()

    @method_decorator(token_requerido)
    def get(self, request):
        _id = firmar(request)
        usuario = Usuario.objects.get(id=_id)
        registros = Registro.objects.all()
        for registro in registros:
            print(f"id objeto: {registro.id}:")
            print(f"Tracto: {registro.tracto}")
            print(f"Cargado: {registro.cargado}")
            print(f"Hora: {registro.hora}")
            print(f"Fecha: {registro.fecha}")
            print(f"PPU: {registro.ppu}")
            print(f"Contenedor: {registro.contenedor}")
            print(f"Sello: {registro.sello}")
            print(f"Conductor: {registro.idConductor}")
            print(f"Camion: {registro.idCamion}")
            print(f"Usuario: {registro.idUsuario}")
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
        # Obtiene al autor del formulario por completar en base a la sesión iniciada.
        firmado = firmar(request=request)
        autor = Usuario.objects.get(id=firmado)
        # Captura los valores sencillos del formulario.
        tracto = request.POST["tracto"]
        cargado = request.POST.get("cargado", "0")  # Cambiado 0 a "0" para mantener el tipo de dato.
        ppu = request.POST["ppu"]
        
        # Obtiene y procesa los valores complejos del formulario.
        baseFecha = request.POST["fecha"]
        fecha = baseFecha.split("T")[0]
        hora = baseFecha.split("T")[1]
        
        # si cargador = 0 el contenedor y el sello quedan vacios y si es 1 hay que rellenar el contenedor y el sello
        if cargado == "0":
            contenedor = ""  # Contenedor vacío cuando cargado es igual a "0".
            sello = ""  # Sello vacío cuando cargado es igual a "0".
        else:
            # Verificar si comienzoContenedor está presente en request.POST
            # Si no está presente recibe una cadena vacia
            contIni = request.POST.get("comienzoContenedor", "")
            contFin = request.POST.get("finalContenedor", "")
            contenedor = "{}-{}".format(contIni, contFin)
            sello = request.POST["sello"]
        
        # Obtiene los otros registros relacionados del formulario y firma.
        idConductor = Conductor.objects.get(id=request.POST["idConductor"])
        idCamion = Camion.objects.get(id=request.POST["idCamion"])
        idUsuario = autor
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
