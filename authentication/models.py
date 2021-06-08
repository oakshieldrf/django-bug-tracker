# -*- encoding: utf-8 -*-

from django.db import models

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

    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    correo = models.EmailField()
    rol = models.CharField(max_length=20, choices=ROLES_OPCIONES, default='dev')
    fechaRegistro = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices = STATUS_CHOICES, default = 'verificado')
    #password = models.PasswordField()

# Convierte esta clase en una abstracta
    class Meta: 
        abstract = True
    

class ScrumMaster(models.Model):
    pass 

class Desarrollador(models.Model):
    pass 


