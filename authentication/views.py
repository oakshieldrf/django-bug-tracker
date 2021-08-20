# -*- encoding: utf-8 -*-


from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
from .models import UserExtend
import datetime
from django.contrib.auth.decorators import login_required


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Los datos inválidos o tu cuenta esta deshabilitada'    
        else:
            msg = 'Error validando el formulario'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})


def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():

            new_user = form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            new_profile = UserExtend.objects.create(user=new_user)
            horas = datetime.time(00,00,00)
            new_profile.horasTrabajo = horas
            curfechaHora = datetime.datetime.now()
            fh_string = curfechaHora.strftime("%d/%m/%Y %H:%M:%S") 
            new_profile.ultimoUpdate = fh_string
            new_profile.user.groups.add(Group.objects.get(name='desarrollador')) 

            msg     = 'Usuario creado - Por favor <a href="/login" class="font-weight-bold">Inicia sesión</a>.'
            success = True
            
            #return redirect("/login", {"msg" : msg, "success" : success })

        else:
            msg = 'El formulario no es válido'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })
