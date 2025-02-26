from decouple import config


from datetime import timedelta
import os
from pathlib import Path
import dotenv

dotenv.read_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    #admin interface UI
    
    'django.contrib.admin',

    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
        #packages
    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt',
        #app
    'product',
    'account',
    'order',
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

ROOT_URLCONF = 'eshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'eshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.custom_exception_handler.custom_exception_handler',
     'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),  # Access token expires in 15 days
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Refresh token expires in 1 day
    'BLACKLIST_AFTER_ROTATION': True,  # Blacklist old refresh tokens after rotation
    'AUTH_HEADER_TYPES': ('Bearer',),  # Token prefix (Authorization: Bearer <token>)
    'AUTH_TOKEN_CLASSES': ("rest_framework_simplejwt.tokens.AccessToken",),  # Tuple format (with a comma)
}
#Email API/SMTP product




# Setting the backend to use SMTP for email sending.
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Optionally, using console backend for debugging output (instead of sending actual emails).
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Host for the email server; loaded from environment variables for security.
EMAIL_HOST = os.environ.get('EMAIL_HOST')

# Email username from environment variable.
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')

# Email password from environment variable.
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# Port for the SMTP server, typically 587 for TLS or 465 for SSL.
EMAIL_PORT = os.environ.get('EMAIL_PORT')

# Boolean to determine if TLS (Transport Layer Security) should be used; set to False by default.
EMAIL_USE_TLS = False

# Boolean to determine if SSL should be used instead of TLS; also False for now.
EMAIL_USE_SSL = False






from decouple import config

SSLCOMMERZ = {
    "STORE_ID": config("SSLCOMMERZ_STORE_ID"),
    "STORE_PASS": config("SSLCOMMERZ_STORE_PASS"),
    "IS_SANDBOX": config("SSLCOMMERZ_IS_SANDBOX", default=True, cast=bool)
}
