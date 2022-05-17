"""
Django settings for outliers_backend project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from io import StringIO
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv, find_dotenv
from google.cloud.secretmanager import SecretManagerServiceClient


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Configurations loading. 
env_path = find_dotenv()
# If local .env file is available, use that. 
# Otherwise, use one from Google Cloud Secret Manager.
if os.path.isfile(env_path):
    load_dotenv(env_path)
elif os.environ.get('GOOGLE_CLOUD_PROJECT', None):
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')

    client = SecretManagerServiceClient()
    settings_name = os.environ.get('SETTINGS_NAME', 'django_settings')
    name = f'projects/{project_id}/secrets/{settings_name}/versions/latest'
    payload = client.access_secret_version(name=name).payload.data.decode('UTF-8')
    configs = StringIO(payload)
    load_dotenv(stream=configs)
else:
    raise Exception("No local .env or Google Cloud Secret Manager found. No secrets found.")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('PRODUCTION') == 'FALSE'

# ALLOWED_HOSTS = [
#     'localhost', 
#     '127.0.0.1',
#     '.outliers-350303.du.r.appspot.com',
#     '.frontend-dot-outliers-350303.du.r.appspot.com',
#     '.getoutliers.com',
# ]
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'https://getoutliers.com',
    'https://api.getoutliers.com',
    'https://outliers-350303.du.r.appspot.com'
    'https://frontend-dot-outliers-350303.du.r.appspot.com'
]
# CORS_ORIGIN_ALLOW_ALL = True    

CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True

APPENGINE_URL = os.getenv('APPENGINE_URL')
if os.getenv('APPENGINE_URL'):
    # Ensure a scheme is present in the URL before it's processed.
    if not urlparse(APPENGINE_URL).scheme:
        APPENGINE_URL = f'https://{APPENGINE_URL}'

    ALLOWED_HOSTS = [urlparse(APPENGINE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [APPENGINE_URL]
    SECURE_SSL_REDIRECT = True


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'github', 
    'scores',
    'technologies',
    'openings',
    'leads',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'django_nose',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'outliers_backend.urls'

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

WSGI_APPLICATION = 'outliers_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_DEFAULT_NAME'),
        'USER': os.getenv('DATABASE_DEFAULT_USER'),
        'PASSWORD': os.getenv('DATABASE_DEFAULT_PASSWORD'),
        'HOST': os.getenv('DATABASE_DEFAULT_HOST'),
        'PORT': os.getenv('DATABASE_DEFAULT_PORT'),
    }
}
 
if os.getenv('PRODUCTION') == 'TRUE' and os.getenv('GITHUB_ACTIONS_WORKFLOW') == 'FALSE':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DATABASE_PRODUCTION_NAME'),
            'USER': os.getenv('DATABASE_PRODUCTION_USER'),
            'PASSWORD': os.getenv('DATABASE_PRODUCTION_PASSWORD'),
            'HOST': os.getenv('DATABASE_PRODUCTION_HOST'),
            'PORT': os.getenv('DATABASE_PRODUCTION_PORT'),
        }
}

if os.getenv('GITHUB_ACTIONS_WORKFLOW') == 'TRUE':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DATABASE_GITHUB_ACTIONS_NAME'),
            'USER': os.getenv('DATABASE_GITHUB_ACTIONS_USER'),
            'PASSWORD': os.getenv('DATABASE_GITHUB_ACTIONS_PASSWORD'),
            'HOST': os.getenv('DATABASE_GITHUB_ACTIONS_HOST'),
            'PORT': os.getenv('DATABASE_GITHUB_ACTIONS_PORT'),
        }
}

if os.getenv('USE_CLOUD_SQL_AUTH_PROXY') == 'TRUE':
    DATABASES['default']['HOST'] = '127.0.0.1'
    DATABASES['default']['PORT'] = 5432


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=users,github,scores,technologies',
    '--cover-html',
]
