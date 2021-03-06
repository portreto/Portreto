"""
Django settings for PORTRETO project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hjx$r7!2@!e*yx%$0d!oa8$9o=tilgtqgdmqeld1rmbf7^$iu='

SESSION_COOKIE_NAME = "web-app-cookie"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'bootstrap4',
    'crispy_forms', #crispy used to styles forms
    'users.apps.UsersConfig',
    'webmain.apps.WebmainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
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

ROOT_URLCONF = 'PORTRETO.urls'

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

WSGI_APPLICATION = 'PORTRETO.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'REPLICASET': 'rs0',
#         'NAME': 'appdata',
#         'HOST': ['mongodb://portreto:portreto@mongo-rs0-1/appdata','mongodb://portreto:portreto@mongo-rs0-2/appdata','mongodb://portreto:portreto@mongo-rs0-3/appdata'],
#         'PORT': 27017,
#         'AUTH_MECHANISM': 'SCRAM-SHA-256',
#         'USER': 'portreto',
#         'PASSWORD': 'portreto',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

"SK EDITS"

MEDIA_ROOT = os.path.join(BASE_DIR ,'media') #Media root is the full path to the directory where django stores files
MEDIA_URL = '/media/' #This is how we are going to see this in the url
CRISPY_TEMPLATE_PACK = 'bootstrap4' # Default crispy form is bootstrap 2.Change it to 4

LOGIN_REDIRECT_URL = 'webmain:index'    #As we use the default backend django form we need to change the default path to be redirected after login
#LOGIN_LOGIN = 'users:login'

STORAGE_SERVER = "storage_1"
KEY = "lol"

GLOBALS = {"hash_key":"init"}

ZOOCLIENTS = "zoo1:2181,zoo2:2181,zoo3:2181"