from django.db import models
import re
import string
import bcrypt
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UsuarioManager(models.Manager):
    def validaciones_basicas(self, postData):
        puntuacion = string.punctuation + "¡¿1234567890"
        errores = {}
        if len(postData["first_name"])<2:
            errores['first_name_largo']="Nombre debe tener al menos 2 caracteres"
        for i in postData["first_name"]:
            if i in puntuacion:
                if 'first_name_letras' not in errores:
                    errores['first_name_letras']="Nombre no debe contener caracteres, solo letras"
        if len(postData["last_name"])<2:
            errores['last_name_largo']="Apellido debe tener al menos 2 caracteres"
        for i in postData["last_name"]:
            if i in puntuacion:
                if 'last_name_letras' not in errores:
                    errores['last_name_letras']="Apellido no debe contener caracteres, solo letras"
        
        if datetime.strptime(postData["cumpleaños"],'%Y-%m-%d') > datetime.now():
            errores["cumple"]="Ingrese fecha de nacimiento válida"

        edad = relativedelta(datetime.now(), datetime.strptime(postData["cumpleaños"],'%Y-%m-%d'))
        if edad.years < 13:
            errores["edad"] = "Tienes que esperar a tener 13 años"

        if len(postData["email"])<1:
            errores["largo_email"] = "Debe ingresar algun email"
        if len(postData["password"])<8:
            errores["largo_contraseña"]="La contraseña debe tener al menos 8 caracteres"
        if postData["password"] != postData["confirm_password"]:
            errores["contraseñas"]="Las contraseñas no coinciden"
        
        elif not EMAIL_REGEX.match(postData['email']):
            errores['email']= "Email no es válido"
        
        usuario = Usuario.objects.filter(email=postData["email"])
        if len(usuario)>0:
            errores["ya_existe"]="El correo utilizado ya tiene una cuenta"

        return errores
    
    def validaciones_login(self, postData):
        errores = {}
        if len(postData["email"]) == 0:
            errores["largo_email"] = "Debe ingresar algun email"
        if len(postData["password"])<8:
            errores["largo_contraseña"]="La contraseña debe tener al menos 8 caracteres"
        mail_existe = Usuario.objects.filter(email=postData["email"])
        if not len(mail_existe)>0:
            errores["mail_no_existe"]="Este mail no está registrado"
        elif not bcrypt.checkpw(postData['password'].encode(), mail_existe[0].password.encode()):
            errores['password']='Password incorrecta'
        return errores
            



class Usuario(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    cumpleaños = models.DateField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsuarioManager()


