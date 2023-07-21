from django.utils.decorators import method_decorator
from appUsuarios.utils import token_requerido, firmar
from .models import Conductor, Camion, Registro
from appUsuarios.models import Usuario
from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime

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
    @method_decorator(token_requerido)
    def get(self, request):
        _id = firmar(request)
        usuario = Usuario.objects.get(id=_id)
        tracto=request.session.get("tracto",None)
        if tracto:
            registros = Registro.objects.filter(tracto=request.session["tracto"])
        else:
            registros = Registro.objects.all()

        for reg in registros:
            if reg.cargado == 0:
                setattr(reg, "conductor", "{}".format(reg.idConductor.nombre))
                setattr(reg, "camion", "{}".format(reg.idCamion.nombre))
                setattr(reg, "estado", "Vacío")
            else:
                setattr(reg, "conductor", "{}".format(reg.idConductor.nombre))
                setattr(reg, "camion", "{}".format(reg.idCamion.nombre))
                setattr(reg, "estado", "Cargado")
        return render(request, 'registros.html', {
            "nombre":usuario.nombre,
            "registros":registros,
        })
    
    @method_decorator(token_requerido)
    def post(self, request):
        request.session["tracto"] = request.POST["tracto"]
        return redirect("registros")

class NuevoRegistroView(View):
    @method_decorator(token_requerido)
    def get(self, request):
        _id = firmar(request)
        usuario = Usuario.objects.get(id=_id)
        # Junta algunos de los datos necesarios para completar el formulario.
        conductores = Conductor.objects.all()
        camiones = Camion.objects.all()
        # Obtiene al autor del formulario por completar en base a la sesión iniciada.
        firmado = firmar(request=request)
        autor = Usuario.objects.get(id=firmado)
        return render(request, 'nuevoRegistro.html', {
            "nombre":usuario.nombre,
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
        fecha = datetime.now().date()
        hora = datetime.now().time()              
        # Valida si el camión esta cargado para completar el contenedor y el sello.
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
            hora=str(hora).split(".")[0],
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
