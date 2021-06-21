# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from app import views

app_name = 'app'

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),
    path('incidencias/', views.IncidenciasView.as_view(), name='incidencias_list'),
    path('incidencia/<id>/', views.IncidenciaDetalleView.as_view(), name='incidencia_detalle'),
    path('equipos/', views.EquiposView.as_view(), name='equipos_list'),
    path('equipo/<id>', views.EquipoDetailView.as_view(), name='equipo_detalle'),

]
