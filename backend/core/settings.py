# backend/core/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv
import sys # Import sys for database testing setup
import dj_database_url # Import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file located in the parent directory (mech-mashup/.env)
dotenv_path = BASE_DIR.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)
print(f"Loading .env from: {dotenv_path}") # Optional: Add print statement for debugging .env loading

# Quick-start development settings - unsuitable for production
# https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
# Add a fallback for initial setup or if .env is missing temporarily
if not SECRET_KEY:
    print("WARNING: DJANGO_SECRET_KEY not found in environment. Using a temporary insecure key.")
    SECRET_KEY = 'temporary-insecure-key-for-initial-setup'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# Allowed hosts: Get from environment variable, split string by space
ALLOWED_HOSTS_STRING = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1') # Default added
ALLOWED_HOSTS = ALLOWED_HOSTS_STRING.split(' ') if ALLOWED_HOSTS_STRING else []
# Ensure 'backend' service name is allowed if accessed internally within Docker network
if 'backend' not in ALLOWED_HOSTS:
     ALLOWED_HOSTS.append('backend')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',           # Django REST Framework
    'rest_framework_simplejwt', # JWT Authentication
    'corsheaders',              # Cross-Origin Resource Sharing

    # Local apps
    'users.apps.UsersConfig', # Use AppConfig for clarity (points to users/apps.py)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS Middleware - place high up
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Optional: project-wide templates dir
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = os.environ.get('DATABASE_URL')

# Configuration for database access
# Handles tests (SQLite), normal Docker operation (Postgres from DATABASE_URL),
# and fallback (SQLite) if DATABASE_URL is missing outside Docker.
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    # Use SQLite for tests for speed and simplicity
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db_test.sqlite3', # Use a separate file for test DB
        }
    }
elif DATABASE_URL:
    # Use dj_database_url to parse the DATABASE_URL from .env
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600, # Number of seconds database connections should persist
            conn_health_checks=True, # Enable Django's connection health checks
            # ssl_require=False # Set to True if your prod DB uses SSL
        )
    }
    print("Database configured using DATABASE_URL.") # Optional debug print
else:
    # Fallback if DATABASE_URL is not set (e.g., local run without Docker or missing .env)
    print("WARNING: DATABASE_URL not found in environment. Falling back to local SQLite database (db_local.sqlite3).")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db_local.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'de-de' # Changed to German as default

TIME_ZONE = 'Europe/Berlin' # Changed to Berlin time zone

USE_I18N = True

USE_TZ = True # Recommended to keep True for timezone-aware datetimes


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
# Directory where collectstatic will gather files for Nginx to serve in production/staging
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Optional: Directories where Django looks for static files during development
# STATICFILES_DIRS = [ BASE_DIR / 'static' ]


# Media files (User uploaded content)
# https://docs.djangoproject.com/en/4.2/topics/files/

MEDIA_URL = '/media/'
# Directory where user uploads will be stored on the filesystem
MEDIA_ROOT = BASE_DIR / 'mediafiles'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Custom User Model ---
AUTH_USER_MODEL = 'users.CustomUser' # Point to our custom user model


# --- Django REST Framework (DRF) Settings ---
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Use JWT for authentication primarily
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # SessionAuthentication can be useful for the Browsable API if enabled
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # Default to read-only for anonymous users, full access for authenticated
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_RENDERER_CLASSES': ( # Use a tuple or list here
        'rest_framework.renderers.JSONRenderer',
        # Add BrowsableAPIRenderer only during DEBUG for easier development/testing via browser
        # Important: Remove or disable this in production for security.
        ('rest_framework.renderers.BrowsableAPIRenderer' if DEBUG else None),
    ),
    # Optional: Add pagination, filtering, etc. later
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10
}

# --- Filter out None from DEFAULT_RENDERER_CLASSES ---
# This needs to be done *after* the dictionary is defined.
# Convert to list first if you used a tuple, to allow modification
renderers = list(REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'])
# Use a list comprehension to create a new list without None
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [r for r in renderers if r is not None]


# --- Simple JWT Settings ---
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # How long access tokens are valid
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    # How long refresh tokens are valid
    'ROTATE_REFRESH_TOKENS': False, # If True, a new refresh token is issued when you use a refresh token
    'BLACKLIST_AFTER_ROTATION': True, # Blacklist old refresh token after rotation (requires setup if used)

    'UPDATE_LAST_LOGIN': True, # Update user's last_login field upon login via token obtain

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY, # Uses the Django SECRET_KEY
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',), # Expect "Authorization: Bearer <token>"
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id', # Field name on the User model to use as the identifier
    'USER_ID_CLAIM': 'user_id', # Claim name in the JWT payload for the user ID
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5), # For sliding tokens only
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1), # For sliding tokens only
}


# --- CORS (Cross-Origin Resource Sharing) Settings ---
# https://github.com/adamchainz/django-cors-headers

# Allow requests from the Next.js frontend development server
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",   # Default Next.js dev port
    "http://127.0.0.1:3000",
    "http://localhost:8080",   # Nginx port we'll use to access the app
    "http://127.0.0.1:8080",
    # Add the frontend container name if direct communication is needed (usually not)
    # "http://frontend:3000"
]

# Alternatively, allow all origins during development (less secure, easier for testing)
# if DEBUG:
#     CORS_ALLOW_ALL_ORIGINS = True

# If your frontend needs to send cookies or Authorization headers (which it does for JWT)
CORS_ALLOW_CREDENTIALS = True

# You might want to restrict headers and methods in production, e.g.:
# CORS_ALLOW_HEADERS = list(default_headers) + ['my-custom-header']
# CORS_ALLOW_METHODS = list(default_methods) + ['PATCH']

# Logging configuration (optional but useful)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO', # Adjust level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
         'django.db.backends': { # Show SQL queries if DEBUG is True
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}