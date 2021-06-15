from django.urls import path
from . import views

urlpatterns = [
    path('<int:id_usuario>', views.index),
    path('post_mensaje/<int:id_usuario>',views.post_mensaje),
    path('post_comentario/<int:id_usuario>/<int:id_mensaje>',views.post_comentario),
    path('delete_comentario/<int:id_comentario>',views.delete_comentario),
]