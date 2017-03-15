"""geocoder_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from geocoder.views import InterseccionView, AlturaView, NombresCallesView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^interseccion/$', InterseccionView.as_view(), name='geocoder_interseccion'),
    url(r'^altura_calle/$', AlturaView.as_view(), name='geocoder_altura_calle'),
    url(r'^nombres_calles/$', NombresCallesView.as_view(), name='geocoder_nombres_calles'),
]
