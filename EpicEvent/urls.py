from __future__ import division
from django.contrib import admin
from django.urls import path, include


def trigger_error(request):
    division_by_zero = 1 / 0
    print(division_by_zero)
    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("core.urls")), 
    path('api/', include("contracts.urls")),
    path('api/', include("client.urls")),
] 
