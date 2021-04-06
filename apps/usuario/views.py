import json
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.list import ListView, View
from django.contrib.auth.views import LoginView
from .forms import FormularioUsuario, FormularioLogin
from django.contrib.auth import login
from .models import Usuario
from django.http import HttpResponse


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


class InicioListarUsuarios(TemplateView):
    template_name = "usuario/listar_usuarios.html"


class ListarUsuarios(View):
    model = Usuario
    form_class = FormularioUsuario

    def get_queryset(self):
        return self.model.objects.filter(usuario_activo=True)

    def get_context_data(self, **kwargs):
        context = {}
        context["usuarios"] = self.get_queryset()
        context["form"] = self.form_class
        return context

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect("index")

        # Implementación de AJAX en django
        #Hay que crear una lista de los usuarios que se van a madnar al template mediante ajax
        if request.is_ajax():
        # Forma manual de obtener datos tipo json
        #     lista_usuarios=[]
        #     for usuario in self.get_queryset():
        #         data_usuario = {}
        #         data_usuario["id"] = usuario.id
        #         data_usuario["nombres"] = usuario.nombres
        #         data_usuario["apellidos"] = usuario.apellidos
        #         data_usuario["email"] = usuario.email
        #         data_usuario["username"] = usuario.username
        #         data_usuario["usuario_activo"] = usuario.usuario_activo
        #         lista_usuarios.append(data_usuario)
            #Una vez guardados los datos de cada usuario hay que convertir esa lista en formato JSON 
        #        data = json.dumps(lista_usuarios)
            data = serialize("json", self.get_queryset())
            return HttpResponse(data,content_type= "application/json")
        else:
            #Se pone eso ya que al volver atrás a esta página retornaba el archivo JSON, con eso se soluciona el error
            return redirect("inicio_usuarios")

class CrearUsuario(CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = "usuario/crear_usuario.html"
    success_url = reverse_lazy("listar_usuarios")

    # Se sobre escribe el método post para poder guardar el usuario en la DB directamente con cleaned data
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nuevo_usuario = Usuario(
                # Con cleaned_data se obtiene la información validada
                # email = form.cleaned_data.get("email") Es lo mismo
                email=form.cleaned_data["email"],
                username=form.cleaned_data["username"],
                nombres=form.cleaned_data["nombres"],
                apellidos=form.cleaned_data["apellidos"],
            )
            # La contraseña se pone en otro apartado, para que django
            # Realice el proceso de encriptacion
            nuevo_usuario.set_password(form.cleaned_data["password1"])
            nuevo_usuario.save()
            return redirect("listar_usuarios")
        else:
            return render(request, self.template_name, {"form": form})


class EditarUsuario(UpdateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = "usuario/editar_usuario.html"
    success_url = reverse_lazy("listar_usuarios")


class EliminarUsuario(DeleteView):
    model = Usuario
    template_name = "usuario/eliminar_usuario.html"
    success_url = reverse_lazy("listar_usuarios")

    def post(self, request, *args, **kwargs):
        object = self.model.objects.get(id=self.kwargs["pk"])
        object.usuario_activo = False
        object.save()
        return redirect("listar_usuarios")
