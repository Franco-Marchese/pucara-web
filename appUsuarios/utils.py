from django.shortcuts import redirect
from .models import Usuario
from pucaraweb.settings import SECRET_KEY
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import re
from functools import reduce
import pandas as pd
import hashlib
import jwt

def encrypt(pw):
    hasher = hashlib.sha256()
    hasher.update(pw.encode('utf-8'))
    encrypted = hasher.hexdigest()
    return encrypted

def validate(email, password):
    correo = email
    user = Usuario.objects.get(email=correo)
    if user is not None:
        dbPassword = user.contraseña
        if dbPassword == password:
            return user
        else:
            return None
    else:
        return None

class Usuarios:
    # DATOS
    # Función para obtener datos del usuario activo.
    def infoPersonal(self, request):
        token = request.COOKIES["token"]
        decodificando = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        _id = decodificando["id"]
        try:
            user = Usuario.objects.get(id=_id)
        except:
            print("Falló la búsqueda de los datos.")
            return redirect("users")
        return user
    
    # ADMINISTRACIÓN
    # Función para crear usuarios.
    def crearUsuario(self, **kwargs):
        self.email = kwargs.get("email")
        self.nombre = kwargs.get("nombre")
        self.telefono = kwargs.get("telefono", "")
        self.equipo = kwargs.get("equipo")
        self.esAdmin = kwargs.get("esAdmin", 0)
        self.password = kwargs.get("contraseña")

        existe = Usuario.objects.filter(email=self.email).exists()

        if existe:
            # Redirecciona si el correo ya esta registrado.
            print("El usuario ya existe.")
            return redirect("registrar")
        else:
            # Genera una nueva instancia de Usuario con los datos anteriores.
            nuevoUsu = Usuario.objects.create(     
                email=self.email, 
                contraseña=self.password, 
                telefono=self.telefono,
                nombre=self.nombre,
                equipo=self.equipo,
                es_admin=self.esAdmin,
            )
            # Guarda la nueva instancia creada.
            nuevoUsu.save()
            return redirect("ingreso")
    # Función para listar usuarios.
    def todoUsuario(self, **kwargs):
        self.nombre = kwargs.get("nombre", False)

        if self.nombre:
            try:
                usuarios = Usuario.objects.filter(nombre__icontains=self.nombre).values()
            except:
                print("Fallo la búsqueda filtrada.")
                return redirect("usuarios")
        else:
            try:
                usuarios = Usuario.objects.all().order_by('-id')[:30]
            except:
                print("Falló la busqueda de todos.")
                return redirect("usuarios")
        return usuarios
    # Función para eliminar usuarios.
    def eliminarUsuario(self, **kwargs):
        self._id = kwargs.get("_id", False)

        if self._id:
            idSeleccionado = Usuario.objects.get(id=self._id)
            idSeleccionado.delete()

    # VALIDACIÓN
    # Función para autorizar un usuario.
    def autorizarUsuario(self, **kwargs):
        self.correo = kwargs.get("correo", "None")
        self.contraseña = kwargs.get("contraseña", "None")

        existe = Usuario.objects.filter(email=self.correo).exists()

        if existe:
            usuario = validate(email=self.correo, password=self.contraseña)
            if usuario:
                # idProyecto = request.session.get("titulo", None)
                # if idProyecto is not None:
                #     request.session["titulo"] = None
                token = jwt.encode({"id": usuario.id}, SECRET_KEY, algorithm="HS256")
                response = redirect("registros")
                response.set_cookie("token", token, max_age=86400)
                return response
            else:
                # Redirecciona si no es valido.
                return redirect("ingreso")
        else:
            # Redirecciona si el correo no esta registrado.
            return redirect("ingreso")
    # Función para desautorizar un usuario.
    def desautorizarUsuario(self):
        response = redirect("ingreso")
        response.delete_cookie("token")
        return response

def token_requerido(metodo_vista):
    def vista_envuelta(request, *args, **kwargs):
        if "token" not in request.COOKIES:
            return redirect("ingreso")  # Redirect to the login page or a custom URL
        return metodo_vista(request, *args, **kwargs)
    return vista_envuelta

class ModUsuario:

    def cambiaremail(self, **kwargs):
        self._id = kwargs.get("_id", "None")
        self.email = kwargs.get("email", "None")
        emailvalido= validaremail(self.email)
        if emailvalido:
            usuario = Usuario.objects.get(id=self._id)
            usuario.email = self.email
            usuario.save(update_fields=['email'])
            return redirect("mod-usuario")
        else:
            return redirect("mod-usuario")
        
    def cambiartelefono(self, **kwargs):
        self._id = kwargs.get("_id", "None")
        self.telefono = kwargs.get("telefono", "None")
        telefonovalido= validar_numero(self.telefono)
        if telefonovalido:
            usuario = Usuario.objects.get(id=self._id)
            usuario.telefono = self.telefono
            usuario.save(update_fields=['telefono'])
            return redirect("mod-usuario")
        else:
            return redirect("mod-usuario")
        
    def cambiarContraseña(self, **kwargs):
        self._id = kwargs.get("_id", "None")
        self.contraseñaActual = kwargs.get("contraseñaActual", "None")
        self.contraseñaNueva = kwargs.get("contraseñaNueva", "None")
        self.repiteContraseñaNueva = kwargs.get("repiteContraseñaNueva", "None")

        try:
            usuario = Usuario.objects.get(id=self._id)
        except:
            print("No se encontró el usuario")
            return redirect("mod-usuario")

        if encrypt(self.contraseñaActual) == usuario.contraseña:
            if self.contraseñaNueva == self.repiteContraseñaNueva:
                usuario.contraseña = encrypt(self.contraseñaNueva)
                usuario.save(update_fields=['contraseña'])
                return redirect('ingreso')
            else:
                return redirect("mod-usuario-pass")
        else:
            return redirect("mod-usuario-pass")
        

def validaremail(email):
    validar = EmailValidator()
    try:
        validar(email)
        return True
    except ValidationError:
        return False
def validar_numero(telefono):
    patron = r'^\d{9}$'
    if re.match(patron, telefono):
        return True
    else:
        return False


