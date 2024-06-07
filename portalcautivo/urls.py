"""
URL configuration for portalcautivo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from portal.views import *
from contel.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bnc', connect, name="Auto-Login Guest User"),
    path('redirect',redirect,name='Redirect'),
    path('bnc2',connect_contel,name="Auto-Login Guest Contel"),
    path('contel_redirect',redirect_contel, name="Redirect en Contel")
    
]

#path('bnc2',connect_contel,name="Auto-Login Guest Contel"),
#path('contel_redirect',redirect_contel, name="Redirect en Contel")