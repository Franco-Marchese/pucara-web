from django.utils.decorators import method_decorator
from appUsuarios.utils import token_requerido, Usuarios
from .utils import Registros
from .models import Conductor, Camion, Registro
from appUsuarios.models import Usuario
from django.shortcuts import render, redirect
from django.views import View
# Para poblar.
import random
from datetime import datetime, timedelta
from django.utils import timezone
        
class VerRegistrosView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.u = Usuarios()
        self.r = Registros()

    @method_decorator(token_requerido)
    def get(self, request):
        usuario = self.u.infoPersonal(request)
        tracto = request.session.get("tracto", None)
        registros = self.r.listarRegistros(tracto=tracto)
        
        return render(request, 'registros.html', {
            "usuario": usuario,
            "registros":registros,
        })

    @method_decorator(token_requerido)
    def post(self, request):
        tracto = request.POST.get("tracto", "")
        if tracto != "":
            request.session["tracto"] = tracto
            return redirect("registros")
        request.session["tracto"] = None
        return redirect("registros")

class NuevoRegistroView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.u = Usuarios()
        self.r = Registros()

    @method_decorator(token_requerido)
    def get(self, request):
        usuario = self.u.infoPersonal(request)
        conductores = Conductor.objects.all()
        camiones = Camion.objects.all()

        return render(request, 'nuevoRegistro.html', {
            "usuario":usuario,
            "conductores":conductores,
            "camiones":camiones,
        })
    
    @method_decorator(token_requerido)
    def post(self, request):
        self.r.anotarRegistro(
            tracto = request.POST.get("tracto", None),
            cargado = request.POST.get("cargado", False),
            ppu = request.POST.get("ppu", None),
            idConductor = request.POST.get("idConductor", ""),
            idCamion = request.POST.get("idCamion", ""),
            sello = request.POST.get("sello", ""),
            comienzoContenedor = request.POST.get("comienzoContenedor", ""),
            finalContenedor = request.POST.get("finalContenedor", ""),
        )

        return redirect("registros")

class PoblandoView(View):
    def get(self, request):
        # Get the list of available conductors and camions from the database
        conductors = Conductor.objects.all()
        camions = Camion.objects.all()

        # Generate 4200 rows for the Registro model
        for _ in range(4200):
            # Sample data for the row
            tracto = random.randint(1, 1000)
            cargado = random.choice([True, False])
            hora = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
            fecha = (timezone.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
            ppu = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(6))
            contenedor = f"{random.randint(1000000000, 9999999999)}-{random.randint(1, 9)}"
            sello = f"fgdf{random.randint(1000, 9999)}"

            # Randomly select conductor and camion from the available choices
            conductor = random.choice(conductors)
            camion = random.choice(camions)

            # Create the Registro object and save it to the database
            registro = Registro(
                tracto=tracto,
                cargado=cargado,
                hora=hora,
                fecha=fecha,
                ppu=ppu,
                contenedor=contenedor,
                sello=sello,
                idConductor=conductor,
                idCamion=camion,
            )
            registro.save()

        return redirect("ingreso")