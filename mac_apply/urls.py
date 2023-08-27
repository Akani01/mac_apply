# urls to main project
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('theblog/', include('theblog.urls')),
    path('photos/', include('photos.urls')),
    path('broker/', include('broker.urls')),
    path('members/', include('members.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include("django.contrib.auth.urls")),

    #ecommerce colors
    #path('ecommerce/', include('ecommerce.urls')),
  


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
