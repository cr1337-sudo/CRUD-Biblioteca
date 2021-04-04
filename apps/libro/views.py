from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import AutorForm, LibroForm
from .models import Autor, Libro
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from django.contrib.auth.forms import UserCreationForm


# Create your views here.




class Inicio(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class ListarAutor(LoginRequiredMixin, View):
    model = Autor
    form_class = AutorForm
    template_name = "libro/autor/listar_autor.html"

    def get_queryset(self):
        return self.model.objects.filter(estado=True)

    def get_context_data(self, **kwargs):
        context = {}
        context["autores"] = self.get_queryset()
        context["form"] = self.form_class
        return context



    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class EditarAutor(LoginRequiredMixin, UpdateView):
    model = Autor
    template_name = "libro/autor/editar_autor.html"
    form_class = AutorForm
    success_url = reverse_lazy("libro:listar_autor")
    


class EliminarAutor(LoginRequiredMixin, DeleteView):
    model = Autor
    template_name = "libro/autor/eliminar_autor.html"
    # No se puede usar reverse_lazy ya que se está editando el método post
    #success_url = reverse_lazy("libro:listar_autor")

    # Al ejecutarse el método post del formulario se hace lo siguiente con el autor que estamos borrando
    def post(self, request, pk, *args, **kwargs):
        object = self.model.objects.get(id=pk)
        object.estado = False
        object.save()
        return redirect("libro:listar_autor")

class CrearAutor(CreateView):
    model = Autor
    form_class = AutorForm
    template_name = "libro/autor/crear_autor.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)   
        if form.is_valid():
            form.estado=True
            form.save()
            return redirect("libro:listar_autor")




########################          LIBRO          ###########################

class ListadoLibros(View):
    model = Libro
    template_name = "libro/libro/listar_libro.html"
    form_class = LibroForm

    def get_queryset(self):
        return self.model.objects.filter(estado=True)

    def get_context_data(self, **kwargs):
        context = {}
        context["libros"] = self.get_queryset()
        context["form"] = self.form_class
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class CrearLibro(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = "libro/libro/crear_libro.html"
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("libro:listar_libro")

class EliminarLibro(DeleteView):
    model = Libro
    template_name = "libro/libro/eliminar_libro.html"

    def post(self, request, *args, **kwargs):
        object = self.model.objects.get(id=self.kwargs["pk"])
        object.estado = False
        object.save()
        return redirect("libro:listar_libro")


class EditarLibro(UpdateView):
    model = Libro
    success_url = reverse_lazy("libro:listar_libro")
    template_name = "libro/libro/editar_libro.html"
    form_class = LibroForm
