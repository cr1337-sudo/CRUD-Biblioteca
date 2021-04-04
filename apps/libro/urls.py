from django.urls import path
from .views import *

urlpatterns = [

    path('listar_autor/', ListarAutor.as_view(), name='listar_autor'),
    path("crear_autor/", CrearAutor.as_view(), name="crear_autor"),
    path('editar_autor/<int:pk>', EditarAutor.as_view(), name='editar_autor'),
    path('eliminar_autor/<int:pk>', EliminarAutor.as_view(), name='eliminar_autor'),

    path("listar_libro/", ListadoLibros.as_view(), name="listar_libro"),
    path("crear_libro/", CrearLibro.as_view(), name="crear_libro"),
    path("editar_libro/<int:pk>", EditarLibro.as_view(), name="editar_libro"),
    path("eliminar_libro/<int:pk>", EliminarLibro.as_view(), name="eliminar_libro"),


]
