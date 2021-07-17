from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '********'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'locations',
    'pwa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vaccination.urls'

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

WSGI_APPLICATION = 'vaccination.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

"""
StatMN Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '*****',
        'PORT': '*****',
        'USER': '*****',
        'PASSWORD': '*****',
        'NAME': '*****',
    }
}

"""

if os.getenv('GAE_APPLICATION', None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '******',
            'USER': '******',
            'PASSWORD': '*******',
            'NAME': '*******',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'USER': '******',
            'PASSWORD': '******',
            'NAME': '******',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = [os.path.join(BASE_DIR, 'static'),]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, 'static'),]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '******'
EMAIL_USE_TLS = True
EMAIL_PORT = 00000
EMAIL_HOST_USER = '*******'
EMAIL_HOST_PASSWORD = '********'
DEFAULT_FROM_EMAIL = '********'

PROJECT_NAME = '******'
QUEUE_REGION = '*******'
QUEUE_ID = '*******'
API_KEY = '*******'
ORS_KEY = '*******'

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static', 'assets', 'js', 'serviceworker.js')
PWA_APP_NAME = 'Vaccinations'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_THEME_COLOR = '#F5F5EF'
PWA_APP_BACKGROUND_COLOR = '#F5F5EF'
PWA_APP_START_URL = '/dashboard'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/assets/img/favicon.svg',
        'sizes': '500x500'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/assets/img/vaccine_apple.png',
        'sizes': '180x180'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/splash/iphone5_splash.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    },
        {
        'src': '/static/images/splash/iphone6_splash.png',
        'media': '(device-width: 375px) and (device-height: 667px) and (-webkit-device-pixel-ratio: 2)'
    },
        {
        'src': '/static/images/splash/iphoneplus_splash.png',
        'media': '(device-width: 621px) and (device-height: 1104px) and (-webkit-device-pixel-ratio: 3)'
    },
        {
        'src': '/static/images/splash/iphonex_splash.png',
        'media': '(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3)'
    },
        {
        'src': '/static/images/splash/iphonexr_splash.png',
        'media': '(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 2)'
    },
        {
        'src': '/static/images/splash/iphonexsmax_splash.png',
        'media': '(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 3)'
    },
        {
        'src': '/static/images/splash/ipad_splash.png',
        'media': '(device-width: 768px) and (device-height: 1024px) and (-webkit-device-pixel-ratio: 2)'
    },
        {
        'src': '/static/images/splash/ipadpro1_splash.png',
        'media': '(device-width: 834px) and (device-height: 1112px) and (-webkit-device-pixel-ratio: 2)'
    },
        {
        'src': '/static/images/splash/ipadpro2_splash.png',
        'media': '(device-width: 1024px) and (device-height: 1366px) and (-webkit-device-pixel-ratio: 2)'
    },
        {
        'src': '/static/images/splash/ipadpro3_splash.png',
        'media': '(device-width: 834px) and (device-height: 1194px) and (-webkit-device-pixel-ratio: 2)'
    },
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'