from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from cinetopia import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('', include('cinema.urls')),
    path('', include('shop.urls')),
    path('', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
