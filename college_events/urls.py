from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events import views as event_views

handler404 = 'events.views.error_404_view'
handler500 = 'events.views.error_500_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)