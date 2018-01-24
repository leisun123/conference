"""conference URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
import xadmin
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler404, handler500

handler404 = 'apps.main.views.handler404'
handler500 = 'apps.main.views.handler500'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'', include('activflow.urls')),
    url(r'', include('main.urls')),
    url(r'', include('accounts.urls')),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)