from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", CustomLogin.as_view(), name="login"),
    path("register/", CustomRegister.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("listar_usuarios/", ListarUsuarios.as_view(), name="listar_usuarios"),
]
