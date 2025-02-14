from django.contrib import admin
from django.urls import path, include  # Ensure to import include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('', include('core.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)