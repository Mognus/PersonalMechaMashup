      
# backend/core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Import settings to check DEBUG status
from django.conf.urls.static import static # Import static to serve media/static files in development

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls', namespace='api-users')),
    path('auth/', include('auth_api.urls')), # Using our new auth_api app
]

# --- Serve Static and Media Files during Development ---
if settings.DEBUG:
    # --- Korrektur hier: settings.STATIC_URL statt settings.SETTINGS.STATIC_URL ---
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# --- Optional: Add a simple root view for testing ---
# from django.http import HttpResponse
# def home_view(request):
#     return HttpResponse("<h1>Mech Mashup Backend Root</h1><p>API is at /api/, Auth at /auth/</p>")
# urlpatterns.append(path('', home_view))