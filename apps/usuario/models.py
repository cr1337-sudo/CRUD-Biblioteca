from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, nombres, apellidos, password):
        if not email:
            raise ValueError("El usuario debe tener un correr electrónico")
        usuario = self.model(
            username=username,
            email=self.normalize_email(email),
            nombres=nombres,
            apellidos=apellidos)

        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, email, username, nombres, apellidos, password):
        usuario = self.create_user(
            email,
            username=username,
            nombres=nombres,
            apellidos=apellidos,
            password=password)

        usuario.usuario_administrador = True
        usuario.save()
        return usuario


class Usuario(AbstractBaseUser):
    username = models.CharField(
        "Nombre de usuario", unique=True, max_length=50)
    email = models.EmailField("Email", max_length=100, unique=True)
    nombres = models.CharField("Nombre", max_length=200,
                               blank=True, null=True)
    apellidos = models.CharField(
        "Apellido", max_length=200, blank=True, null=True)
    imagen = models.ImageField("Imagen de perfil", upload_to="perfil/",
                               height_field=None, width_field=None, max_length=200, blank=True, null=True)
    usuario_activo = models.BooleanField("Usuario activo", default=True)
    usuario_administrador = models.BooleanField(
        "Usuario administrador", default=False)
    objects = UsuarioManager()

    # Parametro único que va a diferenciar al usuario
    USERNAME_FIELD = "username"
    # Campos requeridos sí o sí
    REQUIRED_FIELDS = ["email", "nombres", "apellidos"]

    def __str__(self):
        return f"Usuario {self.username}"

    # Retorna True si el usuario tiene permisos específico y si está en True puede acceder al panel de admin de django
    def has_perm(self, perm, obj=None):
        return True
    # Tambien para el panel de admin django

    def has_module_perms(self, app_label):
        return True

    # Verifica si el usuario es administrador o no
    @ property
    def is_staff(self):
        return self.usuario_administrador
