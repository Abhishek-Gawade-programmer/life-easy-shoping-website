
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('easylife-admin/', include('easylife_admin.urls',namespace='easylife_admin')),
    path('', include('base.urls',namespace='base')),
]

