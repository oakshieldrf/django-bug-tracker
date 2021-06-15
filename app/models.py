# -*- encoding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User



#Modelo para equipos
class Equipo(models.Model):
    
    nombre = models.CharField(max_length=50)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    miembros = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="equipo_miembros")
    #proyectos = models
    descripcion = models.TextField(max_length=200)
    horasTrabajo = models.TimeField(auto_now=False, auto_now_add=False)


#Modelo para incidencias
class Incidencia(models.Model):

    TIPO_REQUEST = (
        ("incidencia", "Incidencia"),
        ("mejora", "Mejora"),
    )

    GRADO_CHOICES = (
        ("P1","Crítico"),
        ("P2","Alto"),
        ("P3","Moderado"),
        ("P4","Bajo"),
        ("P5","Informativo"),
    )

    ESTADO_CHOICES = (
        ("abierto","Abierto"),
        ("resuelto","Resuelto"),
        ("cerrado","Cerrado"),
        ("eliminado","Eliminado"),
    ) 

    tituloIncidente = models.CharField(max_length=200)
    tipoSolicitud = models.CharField(choices=TIPO_REQUEST,  max_length=20, default = 'incidencia')
    descripcion = models.TextField(max_length=1000)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sistema_incidencia')
    fechaCreacion = models.DateTimeField(auto_now_add = timezone.now() )
    fechaModificacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(choices = ESTADO_CHOICES, max_length=20, default = "abierto")
    responsable = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="incidencia_responsables")
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='equipo_incidencias', default=None ) 
    severidad = models.CharField(max_length=20, choices = GRADO_CHOICES, default='P5')
    horasEstimadas = models.TimeField(auto_now=False, auto_now_add=False)

    # Crear inicidencia 
    
    # 