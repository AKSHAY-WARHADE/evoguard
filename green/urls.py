
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import re_path as url

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('',include('city.urls')),
    path('admin/', admin.site.urls,name='admin'),
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
]


urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)