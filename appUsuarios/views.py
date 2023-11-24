from .utils import encrypt, token_requerido, Usuarios, ModUsuario
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.views import View
from .models import Usuario

# Create your views here.
class IngresoView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.u = Usuarios()

    def get(self, request):
        if "token" in request.COOKIES:
            desautorizar = self.u.desautorizarUsuario()
            return desautorizar
        return render(request, 'login.html', {})
        
    def post(self, request):
        autorizado = self.u.autorizarUsuario(
            correo=request.POST["email"],
            contraseña=encrypt(request.POST["contraseña"]),
        )
        return autorizado

class EgresoView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.u = Usuarios()

    @method_decorator(token_requerido)
    def get(self, request):
        # Elimina la cookie de inicio de sesión.
        desautorizar = self.u.desautorizarUsuario()
        return desautorizar

class RegistrarView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.u = Usuarios()

    @method_decorator(token_requerido)
    def get(self, request):
        usuario = self.u.infoPersonal(request)
        return render(request, 'registro.html', {
            "usuario":usuario,
        })
    
    @method_decorator(token_requerido)
    def post(self, request):
        self.u.crearUsuario(
            email = request.POST.get("email"),
            nombre = request.POST.get("nombre"),
            equipo = request.POST.get("equipos"),
            telefono = request.POST.get("telefono", ""),
            esAdmin = int(request.POST.get("esAdmin", "0")),
            contraseña = encrypt(request.POST.get("contraseña")),
        )
        return redirect("usuarios")

class UsuariosView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.u = Usuarios()

    @method_decorator(token_requerido)
    def get(self, request):
        nombre = request.session.get("nombre", None)
        # Puede devolver una lista de usuarios completa o filtrada.
        usuarios = self.u.todoUsuario(nombre=nombre)
        usuario = self.u.infoPersonal(request)

        return render(request, 'usuarios.html', {
            "usuario":usuario,
            "usuarios":usuarios,
        })
    
    @method_decorator(token_requerido)
    def post(self, request):
        nombre = request.POST.get("nombre", "")
        if nombre != "":
            request.session["nombre"] = nombre
            return redirect("usuarios")
        request.session["nombre"] = None
        return redirect("usuarios")

class EliminarView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.u = Usuarios()

    @method_decorator(token_requerido)
    def get(self, request, id):
        usu = self.u.infoPersonal(request)
        if id == usu.id:
            print("No se puede auto eliminar de los registros.")
        else:
            self.u.eliminarUsuario(_id=id)
        return redirect('usuarios')
    
        
class ModificarUsuario(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.u = Usuarios()
        self.modu = ModUsuario() 

    @method_decorator(token_requerido)
    def get(self, request):
        usuario = self.u.infoPersonal(request)

        return render(request, 'usuario-mod.html', {
            "usuario": usuario,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "telefono": usuario.telefono,
            "equipo": usuario.equipo
        })
    @method_decorator(token_requerido)
    def post(self, request):
        usuario = self.u.infoPersonal(request)

        if request.POST["email"] != "":
            # Usar la instancia de ModUsuario
            cambiandoemail = self.modu.cambiaremail(
                _id=usuario.id,
                email=request.POST["email"],
            )
            return cambiandoemail
        if request.POST["telefono"] != "":
            # Usar la instancia de ModUsuario
            cambiandotelefono = self.modu.cambiartelefono(
                _id=usuario.id,
                telefono=request.POST["telefono"],
            )
            return cambiandotelefono
        return redirect('mod-usuario') 

class ModPass(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.u = Usuarios()
        self.modu = ModUsuario() 

    @method_decorator(token_requerido)
    def get(self, request):
        # Lógica para obtener información o realizar acciones necesarias
        user = self.u.infoPersonal(request)

        return render(request, 'usuario-mod-pass.html', {
            "user": user,
            "nombre": user.nombre,
        })
    
    @method_decorator(token_requerido)
    def post(self,request):
        cambiando = self.modu.cambiarContraseña(
            _id = request.POST["_id"],
            contraseñaActual = request.POST["contraseñaActual"],
            contraseñaNueva = request.POST["nuevaContraseña"],
            repiteContraseñaNueva = request.POST["repiteNuevaContraseña"],
        )
        return cambiando
        
        

        



        