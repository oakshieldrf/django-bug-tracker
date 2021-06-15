# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .forms import IncidenciaForm
from django.views.generic import View
from .models import Incidencia, Equipo
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



## Vista para pagina de Incidencias
'''@login_required(login_url="/login/")
def incidenciasView(request):
    context = {}
    load_template      = request.path.split('/')[-1]
    context['segment'] = load_template
    html_template = loader.get_template( 'incidencias.html' )

    return HttpResponse(html_template.render(context, request))
'''

#@login_required(login_url="/login/")
class IncidenciasView(View):

    def get(self, request):
        context = {}
        context['segment'] = 'index'

        html_template = loader.get_template( 'incidencias.html' )
        return HttpResponse(html_template.render(context, request))
       
#Crea una incidencia
    def post(self, request): 
        form = IncidenciaForm(request.POST)


        if form.is_valid():
            cd = form.cleaned_data
            nombre = cd['nombre']
            grado = cd['grado']
            descripcion = cd['descripcion']
            #equipo = cd['equipo']
            tipo = cd['tipo']
            responsables = cd['responsables']
            equipo = Equipo.objects.get(pk='1')


        # Crea objeto nuevo Incidencia pero no lo guarda aun 
            incidencia = Incidencia()
            incidencia.tituloIncidente = cd['nombre']
            incidencia.tipoSolicitud = cd['tipo']
            incidencia.descripcion = cd['descripcion']
            incidencia.autor = request.user
            incidencia.responsable = request.user
            incidencia.severidad = cd['grado']
            incidencia.horasEstimadas = cd['horas']
            incidencia.equipo = equipo

            incidencia.save()
            messages.success(request, 'Has añadido una incidencia exitosamente')

               
            return redirect('incidencias_list')

        else: 
            messages.error(request, 'Error, faltaron datos o son inválidos')
   
            return redirect('incidencias_list')

        
        context = {}
        context['segment'] = 'index'

        html_template = loader.get_template( 'incidencias.html' )
        return HttpResponse(html_template.render(context, request))
          