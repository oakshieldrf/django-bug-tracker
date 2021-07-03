# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .forms import IncidenciaForm, EquipoForm
from django.views.generic import View
from .models import Incidencia, Equipo
from authentication.models import UserExtend
from django.utils import timezone
from django.contrib import messages


@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}

    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))



############ Vista para pagina de Incidencias ##########

class IncidenciasView(View):


    def get(self, request):

        listaIncidencias = Incidencia.objects.all()
        equipos = Equipo.objects.all()
        responsables = User.objects.all()
        for user in responsables: 
            print(user.first_name)
        print(listaIncidencias)

        context = {}
        context['segment'] = 'index'
        context['lista_incidentes'] = listaIncidencias #Agrega lista de incidentes al contexto para mostrar en template
        context['equipos'] = equipos
        context['responsables'] = responsables

        html_template = loader.get_template( 'incidencias.html')
        return HttpResponse(html_template.render(context, request))

       
### Crea una incidencia
    def post(self, request): 

        form = IncidenciaForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            nombre = cd['nombre']
            grado = cd['grado']
            descripcion = cd['descripcion']
            equipo = Equipo.objects.get(pk=cd['equipo'])
            tipo = cd['tipo']
            responsables = User.objects.get(pk=cd['responsables'])
            horas = cd['horas']

        # Crea objeto nuevo Incidencia pero no lo guarda aun 
            incidencia = Incidencia()
            incidencia.titulo = nombre
            incidencia.tipo = tipo
            incidencia.descripcion = descripcion
            incidencia.autor = request.user
            incidencia.responsables = responsables
            incidencia.grado = grado
            incidencia.horasEstimadas = horas
            incidencia.equipo = equipo

            incidencia.save()
            messages.success(request, 'Has añadido una incidencia exitosamente')
                       
            return self.get(request)

        else: 
            messages.error(request, 'Error al añadir la incidencia')
            
            return self.get(request)


########## Clase para detalles una incidencia ###########

class IncidenciaDetalleView(View): 

    def get(self, request, id):

        incidencia = Incidencia.objects.get(pk=id)
        equipos = Equipo.objects.filter().exclude(id=incidencia.equipo.id)
        responsables = User.objects.filter().exclude(id=incidencia.responsables.id)
        grado = Incidencia.GRADO_CHOICES

        print(incidencia)
        context = {}
        context['segment'] = 'index'
        context['incidencia'] = incidencia
        context['equipos'] = equipos
        context['responsables'] = responsables
        context['grado'] = grado 
 

        html_template = loader.get_template( 'incidencia-detalle.html' )
        return HttpResponse(html_template.render(context, request))
       
### Modifica detalles de incidencia
    def post(self, request, id): 

        incidencia = Incidencia.objects.get(pk=id)
        dataUpdate = request.POST
        print(dataUpdate)

        incidencia.grado = dataUpdate['grado'] 
        incidencia.titulo = dataUpdate['nombre']
        incidencia.estado = dataUpdate['estado']
        userresponsable = User.objects.get(pk=dataUpdate['responsables'])
        incidencia.responsables = userresponsable
        equiporeponsable = Equipo.objects.get(pk=dataUpdate['equipo'])
        incidencia.equipo = equiporeponsable
        incidencia.descripcion = dataUpdate['descripcion']
        incidencia.tipo = dataUpdate['tipo']
        incidencia.fechaModificacion = timezone.now()

        incidencia.save()


        return self.get(request,id)



##################################################
########### Clase para lista de equipos ##########
##################################################

class EquiposView(View): 

    def get(self, request):

        equipos = Equipo.objects.all()
        
        context = {}
        context['segment'] = 'index'
        context['lista_equipos'] = equipos
        context['miembros'] = User.objects.all().exclude(username='admin')

        return render(request, 'equipos.html', context)
        

    def post(self, request):

        form = EquipoForm(request.POST)

        context = {}
        context['segment'] = 'index'

        if form.is_valid():
            
            cd = form.cleaned_data
            nombre = cd['nombre']
            descripcion = cd['descripcion']
            miembros_id = cd['miembros']
            print(miembros_id)
            miembros = User.objects.get(pk=miembros_id)

            equipoNuevo = Equipo()
            equipoNuevo.nombre = nombre 
            equipoNuevo.fechaCreacion = timezone.now()
            equipoNuevo.miembros = miembros
            equipoNuevo.descripcion = descripcion

            equipoNuevo.save()
            messages.success(request, 'Se ha creado un equipo nuevo')

            return self.get(request)

        else: 

            messages.error(request, 'Error al crear un equipo')

            return self.get(request)


###################################################
########### Clase para detalle de equipo ##########
################################################### 

class EquipoDetailView(View):

    def get(self, request, id):

        equipo = Equipo.objects.get(pk=id)
        incidencias = Incidencia.objects.filter(equipo=equipo)
        miembros = equipo.miembros
        
        context = {}
        context['segment'] = 'index'
        context['equipo'] = equipo
        context['lista_incidentes'] = incidencias
        context['miembros'] = miembros

        return render(request, 'equipo-detalle.html', context)
        

    def post(self, request, id):
        
        equipo = Equipo.objects.get(pk=id)

        dataUpdate = request.POST

        context = {}
        context['segment'] = 'index'
        nombreNuevo = dataUpdate['nombre']
        descripcionNuevo = dataUpdate['descripcion']
        equipo.nombre = nombreNuevo
        equipo.descripcion = descripcionNuevo

        equipo.save()


        return self.get(request,id)


###################################################
########### Clase para lista de usuarios ##########

class UsuariosView(View):

    lista_usuarios = User.objects.all()

    context = {}

    def get(self, request):

        context = {}
        context['segment'] = 'index'
        context['lista_equipos'] =  Equipo.objects.all()
        context['usuarios'] = User.objects.all().exclude(username='admin')

        return render(request, 'usuarios.html', context)

    def post(self,request):
        pass 

###################################################
########### Clase para detalle usuario ############

class UsuarioDetailView(View):


    def get(self, request, id):

        context = {}
        context['segment'] = 'index'
        usuario = User.objects.get(pk=id)
        context['usuario'] = usuario
        roles = usuario.groups.all()
        context['roles'] = roles[0]
        context['equipos'] = Equipo.objects.filter(miembros__id = id)
        context['userextend'] = UserExtend.objects.get(user__id=id)

        return render(request, 'usuario-detalle.html', context)

    def post(self,request,id):

        usuario = User.objects.get(pk=id)

        dataUpdate = request.POST

        usuario.first_name = dataUpdate['nombre']
        usuario.last_name = dataUpdate['apellido']
        usuario.email = dataUpdate['email']

        usuario.save()

        return self.get(request,id)
