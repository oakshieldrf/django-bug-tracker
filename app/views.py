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
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse





@login_required(login_url="/login/")
def index(request):

    incidencias = Incidencia.objects.all()
    ultimasIncidencias = Incidencia.objects.all()[:4]
    equipos = Equipo.objects.all()
    usuarios = User.objects.all()
    

    context = {}
    context['segment'] = 'index'
    context['incidencias'] = incidencias 
    context['ultimasIncidencias'] = ultimasIncidencias
    context['equipos'] = equipos 
    context['usuarios'] = usuarios 


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
        #Paginacion
        paginator = Paginator(listaIncidencias, 10) # 10 incidencia por cada pagina
        page = request.GET.get('page')

        try:
            incidencias = paginator.page(page)  
        
        except PageNotAnInteger:
            #Si la pagina no es un entero mostrar la primer pagina
            incidencias = paginator.page(1)
        
        except EmptyPage:
            #Si la pagina esta fuera del rango mostrar a ultima pagina de resultados
            incidencias = paginator,page(paginator.num_pages)

        context = {}
        context['segment'] = 'index'
        context['lista_incidentes'] = incidencias
        context['equipos'] = equipos
        context['responsables'] = responsables
        context['page'] = page


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
        userIsResponsable = True if incidencia.responsables == request.user else False

        context = {}
        context['segment'] = 'index'
        context['incidencia'] = incidencia
        context['equipos'] = equipos
        context['responsables'] = responsables
        context['grado'] = grado
        context['isResponsable']  = userIsResponsable
 

        html_template = loader.get_template( 'incidencia-detalle.html' )
        return HttpResponse(html_template.render(context, request))
       
### Modifica detalles de incidencia
    def post(self, request, id): 

        incidencia = Incidencia.objects.get(pk=id)
        dataUpdate = request.POST

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
        incidencia.horasEstimadas = dataUpdate['horas']

        incidencia.save()


        return self.get(request,id)



##################################################
########### Clase para lista de EQUIPOS ##########
##################################################

class EquiposView(View): 

    def get(self, request):

        equipos = Equipo.objects.all()
        paginator = Paginator(equipos, 10)
        page = request.GET.get('page')

        try:
            equiposPaginacion = paginator.page(page)
        
        except PageNotAnInteger:
            equiposPaginacion = paginator.page(1)
        
        except EmptyPage:
            equiposPaginacion = paginator.page(paginator.num_pages)
        
        context = {}
        context['segment'] = 'index'
        context['lista_equipos'] = equiposPaginacion #Segmentos de objetos Equipo para mostrar en su respectiva pagina
        context['miembros'] = User.objects.all().exclude(username='admin')
        context['page'] = page

        html_template = loader.get_template( 'equipos.html')
        return HttpResponse(html_template.render(context, request))


    def post(self, request):

        form = EquipoForm(request.POST)

        context = {}
        context['segment'] = 'index'

        if form.is_valid():
            
            cd = form.cleaned_data
            nombre = cd['nombre']
            descripcion = cd['descripcion']
            miembros_id = cd['miembros']
            miembros = User.objects.get(pk=miembros_id)

            equipoNuevo = Equipo()
            equipoNuevo.nombre = nombre 
            equipoNuevo.fechaCreacion = timezone.now()
            equipoNuevo.descripcion = descripcion

            equipoNuevo.save()
            equipoNuevo.miembros.add(miembros)
            equipoNuevo.save()
            
            messages.success(request, 'Se ha creado un equipo nuevo')

            return self.get(request)

        else: 

            messages.error(request, 'Error al crear un equipo')

            return self.get(request)


###################################################
########### Clase para detalle de EQUIPO ##########
################################################### 

class EquipoDetailView(View):

    def get(self, request, id):

        equipo = Equipo.objects.get(pk=id)
        incidencias = Incidencia.objects.filter(equipo=equipo)
        miembros = equipo.miembros.all()
        es_manager = True if request.user.groups.all()[0].name == 'project-manager'  else False
        usuarios = User.objects.exclude(id__in=[miembro.id for miembro in miembros]).exclude(is_staff=True)

        context = {}
        context['segment'] = 'index'
        context['equipo'] = equipo
        context['lista_incidentes'] = incidencias
        context['miembros'] = miembros
        context['es_manager'] = es_manager
        context['usuarios'] = usuarios

        html_template = loader.get_template( 'equipo-detalle.html')
        return HttpResponse(html_template.render(context, request))
        

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

        messages.success(request, "Datos actualizados correctamente")

        return self.get(request,id)


    #Eliminar equipo
    @require_POST
    def eliminarEquipo(request, id):

        equipo = Equipo.objects.get(pk=id)
        context = {}
        context['nombreEquipo'] = equipo.nombre
        equipo.delete() 

        return render(request, 'equipo-eliminar.html', context)

#Remover miembro del equipo
    @require_POST
    def añadirMiembro(request, id):
        equipo = Equipo.objects.get(pk=id)
        miembroId = request.POST['miembro-nuevo']
        
        miembro = User.objects.get(pk=miembroId)
        equipo.miembros.add(miembro)
        
        messages.success(request, 'Miembro añadido exitosamente')

        return redirect('app:equipo_detalle', id=id)


#Añadir un miembro del equipo
    @require_POST
    def removerMiembro(request, id, idMiembro):
        equipo = Equipo.objects.get(pk=id)
        miembro = User.objects.get(pk=idMiembro)
        equipo.miembros.remove(miembro)
        
        messages.success(request, 'Miembro removido exitosamente')

        return redirect('app:equipo_detalle', id=id)



###################################################
########### Clase para lista de usuarios ##########

class UsuariosView(View):

    def get(self, request):

        lista_equipos = Equipo.objects.all()
        lista_usuarios = User.objects.all().exclude(username='admin')
        #Paginacion
        paginator = Paginator(lista_usuarios, 10)
        page = request.GET.get('page')

        try:
            lista_usuarios = paginator.page(page)
        except PageNotAnInteger:
            lista_usuarios = paginator.page(1)
        except:
            lista_usuarios = paginator.page(paginator.num_pages)

        context = {}
        context['segment'] = 'index'
        context['lista_equipos'] =  lista_equipos
        context['lista_usuarios'] = lista_usuarios
 
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
        context['roles'] = roles[0] if roles else None
        context['equipos'] = Equipo.objects.filter(miembros__id = id)
        context['userextend'] = UserExtend.objects.get(user__id=id)
        grupos = request.user.groups.all()
        context['esmanager'] =  True if grupos[0].name == 'project-manager' else False

        print(request.user.is_active)

        return render(request, 'usuario-detalle.html', context)

    def post(self,request,id):

        usuario = User.objects.get(pk=id)

        dataUpdate = request.POST

        if (not request.POST['estado']): #Evalua si el project manager hizo el request
            usuario.first_name = dataUpdate['nombre']
            usuario.last_name = dataUpdate['apellido']
            usuario.email = dataUpdate['email']

            messages.success(request, "Tus datos han sido actualizados exitosamente")

        else:
            usuario.is_active = dataUpdate['estado']
            messages.success(request, "Los datos han sido actualizados exitosamente")

        usuario.save()

        return self.get(request,id)



#################################################
##############     UTILS   ######################
def notificacionAccion(request):

    context = {}
    #context['mensajeTitulo'] = msgTitulo
    #context['mensajeBody'] = msgBody

    return render(request, "notificacion-accion.html", context )
