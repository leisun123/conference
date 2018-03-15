"""
Django settings for conference project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

SECRET_KEY = 'j9gk(17@_&eqf6itrmams-6alizo=e@$pr81wl2e_mckpg)lyh'

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '47.254.38.1']

ROOT_URLCONF = 'conference.urls'

CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap3'
USE_DJANGO_JQUERY = True

LANGUAGE_CODE = 'en-AS'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True
AUTH_USER_MODEL = 'accounts.Scholar'


STATIC_URL = '/static/'
STATICFILES = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)


LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

PAGE_NUM = 10

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.crispy_forms',
    'DjangoUeditor',
    'apps.accounts',
    'apps.main',
    'gunicorn',
    'apps.smart_selects',
    'apps.PaperReview',
    'channels',
    'channels_redis',
    'apps.chat',
    'guardian',
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
                'django.template.context_processors.media',
                'apps.main.context_processors.sidebar_processor',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'HOST': '47.254.38.1',
        'PORT': '5432',
        'NAME': 'conference',
        'USER': 'wyn',
        'PASSWORD': 'weiaizq1314',
        'ENGINE': 'django.db.backends.postgresql'
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '1178180942@qq.com'
EMAIL_HOST_PASSWORD = 'zaiawbkhnlpujhia'
EMAIL_SUBJECT_PREFIX = 'website'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER


WSGI_APPLICATION = 'conference.wsgi.application'
ASGI_APPLICATION = 'conference.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('47.254.38.1', 6379)],
        },
    },
}



