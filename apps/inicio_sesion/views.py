from django.http.response import HttpResponse
from django.shortcuts import redirect, render, resolve_url
from .models import Usuario
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, "index.html")

def registro(request):
    errores = Usuario.objects.validaciones_basicas(request.POST)
    if len(errores)>0:
        for key, value in errores.items():
            messages.error(request,value)
        return redirect("/")
    else:
        hash1 = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        usuario_nuevo = Usuario.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            cumpleaños = request.POST["cumpleaños"],
            email = request.POST["email"],
            password = hash1
        )
        request.session["id"] = usuario_nuevo.id
        return redirect(f"/wall/{usuario_nuevo.id}")

def login(request):
    errores = Usuario.objects.validaciones_login(request.POST)
    if len(errores)>0:
        for key, value in errores.items():
            messages.error(request,value)
        return redirect("/")
    else:
        usuario = Usuario.objects.get(email=request.POST["email"])
        request.session["id"]=usuario.id
        return redirect(f"/wall/{usuario.id}")

# def success(request, id_usuario):
#     if 'id' not in request.session:
#         return redirect("/")
#     context = {
#         'usuario': Usuario.objects.get(id=id_usuario)
#     }
#     return render(request, "success.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")