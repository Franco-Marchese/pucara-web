from .utils import encrypt, token_requerido, Usuarios
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
            esAdmin = int(request.POST.get("esAdmin", "0")),
            contraseña = encrypt(request.POST.get("contraseña")),
        )
        return redirect("registrar")

class UsuariosView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.u = Usuarios()

    @method_decorator(token_requerido)
    def get(self, request):
        # Puede devolver una lista de usuarios completa o filtrada.
        usuarios = self.u.todoUsuario()
        usuario = self.u.infoPersonal(request)

        return render(request, 'usuarios.html', {
            "usuario":usuario,
            "usuarios":usuarios,
        })

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
        