import re
from django.db import models
from django.db.models.deletion import CASCADE
from datetime import datetime, timedelta, timezone
from django.utils.timezone import now

# Create your models here.
class MensajesManager(models.Manager):
    def validacion_basica_mensajes(self, postData):
        errores = {}
        if len(postData["mensaje"]) == 0:
            errores["mensaje"]="El mensaje debe contener algo"
        return errores

class ComentariosManager(models.Manager):
    def validacion_basica_comentarios(self, postData):
        errores = {}
        if len(postData["comentario"]) == 0:
            errores["comentario"]="El comentario debe contener algo"
        return errores

class Mensajes(models.Model):
    mensaje = models.TextField()
    usuario = models.ForeignKey("inicio_sesion.Usuario", on_delete=CASCADE, related_name="mensajes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MensajesManager()

    class Meta:
        ordering = ['-created_at']


class Comentarios(models.Model):
    comentario = models.TextField()
    mensaje = models.ForeignKey(Mensajes,on_delete=CASCADE,related_name="comentarios")
    usuario = models.ForeignKey("inicio_sesion.Usuario", on_delete=CASCADE, related_name="comentarios_en_mensaje")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ComentariosManager()

    #@property
    def puede_eliminar(self):
        hace_30 = now() - timedelta(minutes=30)
        return self.created_at.replace(tzinfo=None) > hace_30.replace(tzinfo=None)


    class Meta:
        ordering = ['created_at']