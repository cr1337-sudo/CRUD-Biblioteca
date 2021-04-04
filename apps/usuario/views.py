from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView
from .forms import FormularioUsuario, FormularioLogin
from django.contrib.auth import login
from .models import Usuario



# Create your views here.
class CustomLogin(LoginView):
    form_class = FormularioLogin
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("libro:listar_autor")

    

class CustomRegister(FormView):
    template_name = "register.html"
    form_class = FormularioUsuario
    redirect_authenticated_user = True
    success_url = reverse_lazy("libro:listar_autor")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(CustomRegister, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        # Con este if hace el request para saber si el usuario está logeado o no
        if self.request.user.is_authenticated:
            return redirect("libro:listar_autor")
        return super(CustomRegister, self).get(request, *args, **kwargs)


class ListarUsuarios(ListView):
    model = Usuario
    template_name = "usuario/listar_usuarios.html"
    context_object_name = "usuarios"

    def get_queryset(self):
        return self.model.objects.filter(usuario_activo = True)
