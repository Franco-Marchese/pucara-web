from django.shortcuts import redirect
from datetime import datetime
from .models import Conductor, Camion, Registro

class Registros:
    # ADMINISTRACIÓN
    # Función para crear registros.
    def anotarRegistro(self, **kwargs):
        self.tracto = kwargs.get("tracto", None)
        self.cargado = kwargs.get("cargado", False)
        self.ppu = kwargs.get("ppu", None)
        self.fecha = datetime.now().date()
        self.hora = datetime.now().time()  
        self.idConductor = kwargs.get("idConductor")
        self.idCamion = kwargs.get("idCamion")
        self.contIni = kwargs.get("comienzoContenedor", "")
        self.contFin = kwargs.get("finalContenedor", "")
        contenedor = "{}-{}".format(self.contIni, self.contFin)

        if self.cargado:
            sello = kwargs.get("sello", "No recibido")
        else:
            sello = ""

        try:
            idConductor = Conductor.objects.get(id=self.idConductor)
            idCamion = Camion.objects.get(id=self.idCamion)
        except:
            print("Falló la asignación de valores.")
            return redirect("nuevoRegistro")

        nuevoRegistro = Registro.objects.create(
            tracto=self.tracto,
            cargado=self.cargado,
            hora=str(self.hora).split(".")[0],
            fecha=self.fecha,
            ppu=self.ppu,
            contenedor=contenedor,
            sello=sello,
            idConductor=idConductor,
            idCamion=idCamion,
        )
        nuevoRegistro.save()
    # Función para listar registros.
    def listarRegistros(self, **kwargs):
        self.tracto = kwargs.get("tracto", False)

        if self.tracto:
            try:
                registros = Registro.objects.filter(tracto__icontains=self.tracto)
            except:
                print("Fallo la búsqueda filtrada.")
                return redirect("registros")
        else:
            try:
                registros = Registro.objects.all().order_by('-id')[:30]
            except:
                print("Falló la busqueda de todos.")
                return redirect("registros")
            
        for reg in registros:
            setattr(reg, "conductor", "{}".format(reg.idConductor.nombre))
            setattr(reg, "camion", "{}".format(reg.idCamion.nombre))
                
            if reg.cargado:
                setattr(reg, "estado", "Cargado")
            else:
                setattr(reg, "estado", "Vacío")

        return registros