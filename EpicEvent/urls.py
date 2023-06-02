from __future__ import division
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

def trigger_error(request):
    division_by_zero = 1 / 0
    print(division_by_zero)
    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include("core.urls")), 
    path('contracts/', include("contracts.urls")),
    path('client/', include("client.urls")),
] 
