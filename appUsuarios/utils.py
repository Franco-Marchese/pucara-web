from django.shortcuts import redirect
from .models import Usuario
from pucaraweb.settings import SECRET_KEY
import hashlib
import jwt

def verify(email):
    correo = email
    find = Usuario.objects.filter(email=correo).exists()
    return find

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
    
def login(request, usuario):
    token = jwt.encode({"id": usuario.id}, SECRET_KEY, algorithm="HS256")
    response = redirect("menu")
    response.set_cookie("token", token, max_age=86400)
    return response

def logout(request):
    response = redirect("ingreso")
    response.delete_cookie("token")
    return response

def firmar(request):
    token = request.COOKIES["token"]
    firma = jwt.decode(token, SECRET_KEY, algorithms="HS256")
    return firma["id"]

def token_requerido(metodo_vista):
    def vista_envuelta(request, *args, **kwargs):
        if "token" not in request.COOKIES:
            return redirect("ingreso")  # Redirect to the login page or a custom URL
        return metodo_vista(request, *args, **kwargs)
    return vista_envuelta
