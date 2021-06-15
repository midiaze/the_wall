from django.urls import path
from . import views

urlpatterns = [
    path("",views.index),
    path("registro",views.registro),
    path("login",views.login),
    # path("success/<int:id_usuario>",views.success),
    path("logout",views.logout),
]