from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register, 'register'),
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('vehicle/', include('vehicle.urls')),
    path('agency/', include('agency.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
