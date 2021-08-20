# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from app import views

app_name = 'app'


urlpatterns = [
    # The home page
    path('', views.index, name='home'),
     #Utils
    path('notificacion/', login_required(views.notificacionAccion, login_url='/login/'), name='notificacion_accion'),
    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),
    path('incidencias/', login_required(views.IncidenciasView.as_view(), login_url='/login/'), name='incidencias_list'),
    path('incidencia/<id>/', login_required(views.IncidenciaDetalleView.as_view(), login_url='/login/'), name='incidencia_detalle'),
    path('equipos/', login_required(views.EquiposView.as_view(), login_url='/login/'), name='equipos_list'),
    path('equipo/<id>', login_required(views.EquipoDetailView.as_view(), login_url='/login/'), name='equipo_detalle'),
    path('equipo/<id>/eliminar', login_required(views.EquipoDetailView.eliminarEquipo, login_url='/login/'), name='equipo_eliminar'),
    path('equipo/<id>/remover-miembro-<idMiembro>', login_required(views.EquipoDetailView.removerMiembro, login_url='/login/'), name='equipo_del_miembro'),
    path('equipo/<id>/añadir-miembro', login_required(views.EquipoDetailView.añadirMiembro, login_url='/login/'), name='equipo_add_miembro'),
   
    #Vistas de usuarios 
    path('usuarios/', login_required(views.UsuariosView.as_view(), login_url='/login/'), name='usuarios_list'),
    path('usuarios/profile/<id>', login_required(views.UsuarioDetailView.as_view(), login_url='/login/'), name='usuario_detalle'),

   
]

