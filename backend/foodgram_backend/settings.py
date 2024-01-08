# flake8: noqa
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    'SECRET_KEY', '6ixkl2l6l#*ht33mjn&lo_v^ekyfdlyq(uqwepi@35sjq!l)8^'
    )

DEBUG = os.getenv('DEBUG', False)

ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS', '127.0.0.1, localhost'
    ).split(', ')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',

    'users.apps.UsersConfig',
    'subscriptions.apps.SubscriptionsConfig',
    'tags.apps.TagsConfig',
    'ingredients.apps.IngredientsConfig',
    'recipes.apps.RecipesConfig',
    'favorite.apps.FavoriteConfig',
    'shoppingcart.apps.ShoppingcartConfig',
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

ROOT_URLCONF = 'foodgram_backend.urls'

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

WSGI_APPLICATION = 'foodgram_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'USER': os.getenv('DB_USER', 'django'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'NAME': os.getenv('DB_NAME', 'django_db'),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', 5432),

        'ATOMIC_REQUESTS': os.getenv('DB_ATOMIC_REQUESTS', False),
        'AUTOCOMMIT': os.getenv('DB_AUTOCOMMIT', True),
        'CONN_MAX_AGE': os.getenv('DB_CONN_MAX_AGE', 0),
        'CONN_HEALTH_CHECKS': os.getenv('DB_CONN_HEALTH_CHECKS', False),
        'OPTIONS': os.getenv('DB_OPTIONS', {}),
        'TIME_ZONE': os.getenv('DB_TIME_ZONE', None),
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'collected_static'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6,

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ]
}

AUTH_USER_MODEL = 'users.CustomUser'

DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,

    'SERIALIZERS': {
        'user_create': 'users.api.serializers.CustomUserCreateSerializer',
        'user': 'users.api.serializers.CustomUserSerializer',
        'current_user': 'users.api.serializers.CustomUserSerializer',
    },

    'PERMISSIONS': {
        'user': ['rest_framework.permissions.AllowAny'],
        'user_list': ['rest_framework.permissions.AllowAny'],
        'user_create': ['rest_framework.permissions.AllowAny'],
    },
}
