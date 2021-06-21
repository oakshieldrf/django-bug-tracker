# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import Equipo, Incidencia

# Register your models here.

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fechaCreacion', 'descripcion', 'miembros' )
    search_fields = ('miembros',)

@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ('titulo','tipo', 'grado', 'descripcion', 'autor', 'fechaCreacion', 'estado', 'equipo')
    list_filter = ('grado','tipo', 'estado', 'equipo')
    search_fields = ('titulo','equipo')


