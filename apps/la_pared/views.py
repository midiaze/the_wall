from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from apps.inicio_sesion.models import Usuario
from django.contrib import messages
from datetime import datetime, timedelta


# Create your views here.
def index(request, id_usuario):
    if 'id' not in request.session:
        return redirect("/")
    context = {
        'usuario': Usuario.objects.get(id=id_usuario),
        'mensajes' : Mensajes.objects.all(),
        'tiempo_menos_30' :  datetime.now() + timedelta(hours=4)- timedelta(minutes=30), #el 4 es por la diferencia horaria que no se como arreglar
    }
    return render(request, "wall.html", context)

def post_mensaje(request, id_usuario):
    errores = Mensajes.objects.validacion_basica_mensajes(request.POST)
    if len(errores)>0:
        for key, value in errores.items():
            messages.error(request,value, extra_tags=key)
        return redirect(f"/wall/{id_usuario}")
    else:
        mensaje_nuevo = Mensajes.objects.create(
            mensaje = request.POST["mensaje"],
            usuario = Usuario.objects.get(id=id_usuario)
        )
        return redirect(f"/wall/{id_usuario}")

def post_comentario(request, id_usuario, id_mensaje):
    errores = Comentarios.objects.validacion_basica_comentarios(request.POST)
    if len(errores)>0:
        for key, value in errores.items():
            messages.error(request,value, extra_tags=key)
        return redirect(f"/wall/{id_usuario}")
    else:
        comentario_nuevo = Comentarios.objects.create(
            comentario = request.POST['comentario'],
            mensaje = Mensajes.objects.get(id=id_mensaje),
            usuario = Usuario.objects.get(id=id_usuario),
        )
        return redirect(f"/wall/{id_usuario}")

def delete_comentario(request, id_comentario):
    comentario = Comentarios.objects.get(id = id_comentario)
    comentario.delete()
    return redirect(f"/wall/{comentario.usuario.id}")
