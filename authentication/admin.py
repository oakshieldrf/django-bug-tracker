# -*- encoding: utf-8 -*-


from django.contrib import admin
from .models import UserExtend


@admin.register(UserExtend)
class UserAdmin(admin.ModelAdmin):

        list_display = ('user', 'horasTrabajo', 'ultimoUpdate' )
