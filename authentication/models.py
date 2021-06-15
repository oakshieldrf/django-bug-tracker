# -*- encoding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils import timezone

# Clase base para los tipos de usuario
class AbstractUsuario(models.Model):

    ROLES_OPCIONES = (
        ('dev','Desarrollador'),
        ('scrum-master', 'Scrum Master'),
    )

    STATUS_CHOICES = (
        ('verificado', 'Verificado'),
        ('deshabilitado', 'Deshabilitado'),
    )

# Extiende modelo de usuario por default con relacion uno-a-uno
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES_OPCIONES, default='dev')
    fechaRegistro = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices = STATUS_CHOICES, default = 'verificado')
    horasTrabajo = models.TimeField(auto_now=False, auto_now_add=False)
    ultimoUpdate = models.DateTimeField(auto_now=True)

# Convierte esta clase en una abstracta
    class Meta: 
        abstract = True
    

# Modelo para scrum master
class ScrumMaster(AbstractUsuario):
  pass

# Modelo para desarrollador
class Desarrollador(AbstractUsuario):
    pass


