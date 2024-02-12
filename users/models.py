from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Debes ingresar un email para el usuario')
        if not name:
            raise ValueError('Debes ingresar un nombre para el usuario')
        if not last_name:
            raise ValueError('Debes ingresar un apellido para el usuario')
        if password is None:
            raise ValueError('Debes ingresar una contraseña para el usuario')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, last_name, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(null=False, blank=False, unique=True)
    name = models.CharField('Nombre', max_length=50, null=False, blank=False)
    last_name = models.CharField(
        'Apellido', max_length=50, null=False, blank=False)
    age = models.IntegerField('Edad', null=True, blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.name} {self.last_name} {self.id}'
