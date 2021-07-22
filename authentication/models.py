# -*- encoding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils import timezone

# Clase base para los tipos de usuario
class UserExtend(models.Model):

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
    ultimoUpdate = models.DateTimeField(auto_now=True, blank=True, null=True)

