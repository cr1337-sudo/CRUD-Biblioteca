from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", CustomLogin.as_view(), name="login"),
    path("register/", CustomRegister.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("listar_usuarios/", ListarUsuarios.as_view(), name="listar_usuarios"),
    path("crear_usuario/", CrearUsuario.as_view(), name="crear_usuario"),
    path("editar_usuario/<int:pk>", EditarUsuario.as_view(), name="editar_usuario"),
    path("eliminar_usuario/<int:pk>", EliminarUsuario.as_view(), name="eliminar_usuario"),

]
