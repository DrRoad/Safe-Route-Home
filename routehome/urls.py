"""RouteHome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from BestRoute.views import crime_map, location_form
from routehome.views import code, team, about, readme

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', location_form),
    url(r'^map/$', crime_map),
    url(r'^code/$', code),
    url(r'^team/$', team),
    url(r'^about/$', about),
    url(r'^readme/$', readme),
    ]
