from .utils import validate, encrypt, verify, login, logout, token_requerido
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.views import View
from .models import Usuario

# Create your views here.
class IngresoView(View):
    def get(self, request):
        if "token" in request.COOKIES:
            desautorizar = logout(request)
            return desautorizar
        return render(request, 'login.html', {})   
    
    def post(self, request):
        # Devuelve True si el correo ya esta registrado.
        yaExiste = verify(request.POST["email"])
        if yaExiste is True:
            # Rescata los valores enviados por el formulario.
            email = request.POST["email"]
            password = request.POST["contraseña"]
            hashed = encrypt(password)
            # Comprueba la validez de los datos.
            usuario = validate(email=email, password=hashed)
            if usuario is not None:
                print(usuario)
                # Genera una cookie de acceso.
                autorizando = login(request=request, usuario=usuario)
                return autorizando
            else:
                # Redirecciona si no es valido.
                return redirect("ingreso")
        else:
            # Redirecciona si el correo no esta registrado.
            return redirect("ingreso")

class EgresoView(View):
    @method_decorator(token_requerido)
    def get(self, request):
        # Elimina la cookie de inicio de sesión.
        desautorizar = logout(request)
        return desautorizar

class RegistrarView(View):
    # @method_decorator(token_requerido)
    def get(self, request):
        return render(request, 'registro.html', {})
    
    # @method_decorator(token_requerido)
    def post(self, request):
        # Devuelve True si el correo ya esta registrado.
        yaExiste = verify(request.POST["email"])

        if yaExiste is True:
            # Redirecciona si el correo ya esta registrado.
            return redirect("registrar")
        else:
            # Captura los datos del formulario.
            email = request.POST.get("email")
            nombre = request.POST.get("nombre")
            equipo = request.POST.get("equipos")
            esAdmin = request.POST.get("esAdmin", 0)
            converted = int(esAdmin)
            password = request.POST.get("contraseña")
            hashed = encrypt(password)
            # Genera una nueva instancia de Usuario con los datos anteriores.
            nuevoUsu = Usuario.objects.create(     
                email=email, 
                contraseña=hashed, 
                nombre=nombre,
                equipo=equipo,
                es_admin=converted
            )
            # Guarda la nueva instancia creada.
            nuevoUsu.save()
            return redirect("ingreso")

class UsuariosView(View):
    @method_decorator(token_requerido)
    def get(self, request):
        # Busca y devuelve todas las instancias de usuarios en la base de datos.
        usuarios = Usuario.objects.all()
        return render(request, 'usuarios.html', {
            "usuarios":usuarios,
        })

class EliminarView(View):
    @method_decorator(token_requerido)
    def post(self, request, id):
        # Busca al usuario por id del seleccionado.
        idSeleccionado = Usuario.objects.get(id=id)
        # Elimina al usuario encontrado.
        idSeleccionado.delete()
        return redirect('usuarios')
        