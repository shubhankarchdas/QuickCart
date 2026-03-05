"""
Django settings for QCart project.
"""
import os
import socket
from pathlib import Path
from env_config import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Function to get local IP address
def get_local_ip():
    try:
        # Create a socket connection to an external server to get the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        try:
            # Fallback: get hostname and resolve
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return local_ip
        except:
            return "127.0.0.1"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=True, cast=bool)

# Dynamic ALLOWED_HOSTS for development
if DEBUG:
    # Get local IP for mobile access
    LOCAL_IP = get_local_ip()
    ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1', LOCAL_IP]
    # Set SITE_URL dynamically
    SITE_URL = f"http://{LOCAL_IP}:8000"
    print(f"🔗 Development SITE_URL: {SITE_URL}")
    print(f"📱 Access from mobile: {SITE_URL}")
else:
    ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
    SITE_URL = env('SITE_URL', default='https://yourdomain.com')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'QuickCart',
    'category',
    'accounts',
    'store',
    'carts',
    'orders',
    'admin_honeypot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'QCart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links',
                'carts.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'QCart.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ('first_name', 'last_name', 'email'),
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# SMTP Config
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT", cast=int)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
EMAIL_HOST_USER = env("EMAIL_ID")
EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS", cast=bool)

# Session Config
SESSION_ENGINE = env("SESSION_ENGINE")
SESSION_COOKIE_NAME = env("SESSION_COOKIE_NAME")
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", cast=bool)
SESSION_COOKIE_AGE = env("SESSION_COOKIE_AGE", cast=int)
SESSION_EXPIRE_AT_BROWSER_CLOSE = env("SESSION_EXPIRE_AT_BROWSER_CLOSE", cast=bool)

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'accounts': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Print startup info
if DEBUG:
    print("\n" + "="*50)
    print("🚀 QuickCart Development Server")
    print("="*50)
    print(f"📍 Local URL: http://localhost:8000")
    print(f"📱 Mobile URL: {SITE_URL}")
    print(f"🌐 Allowed Hosts: {ALLOWED_HOSTS}")
    print("="*50 + "\n")