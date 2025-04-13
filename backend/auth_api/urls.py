from django.urls import path
# Hier importieren wir die Views direkt aus dem simplejwt Paket
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    # TokenBlacklistView # <-- Optional: uncomment if you set up token blacklisting later
)

# Optional: Namespace für die App
app_name = 'auth_api'

urlpatterns = [
    # Manually define the paths for JWT token handling
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # POST: Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # POST: Refresh token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),   # POST: Verify token

    # Optional: Endpoint for blacklisting refresh tokens (logout mechanism)
    # Needs 'rest_framework_simplejwt.token_blacklist' in INSTALLED_APPS and migrations
    # path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]

# Wichtiger Hinweis: Wenn beim Laden dieser Datei ein ModuleNotFoundError für
# 'rest_framework_simplejwt.views' auftritt, bestätigt das, dass das Paket
# im lokalen Environment fehlt oder nicht gefunden wird.