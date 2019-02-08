"""chopchop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
import chopchop_app.views
import settings as settings

urlpatterns = [


    #BOOKING DEMO - working file only , we pivot this part

    url(r'^admin/', admin.site.urls),
    url(r'^booking$', chopchop_app.views.bookingPage),

    #SENSOR DEMO - submit this part for the functional prototype , the front-end is fully integrate with Database and sensor

    url(r'^get-chair-status$', chopchop_app.views.getChairStatus),

    url(r'^post-chair-status$', chopchop_app.views.postChairStatus),

    #Dashboard_DEMO  -  Dashbord demo for presentation, the front-end visualization use mock data

    url(r'^$', chopchop_app.views.home),
    url(r'^dashboard$', chopchop_app.views.dashboard),

]
