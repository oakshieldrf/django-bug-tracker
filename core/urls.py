# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf import settings 
from django.config.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("authentication.urls")), # Auth routes - login / register
    path("", include("app.urls"))             # UI Kits Html files
] + static(settings.STATIC_URL, document_root =settings.STATIC_ROOT)
