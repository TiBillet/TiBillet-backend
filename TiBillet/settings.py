"""
Django settings for TiBillet project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET')
FERNET_KEY = os.environ.get('FERNET_KEY')

FEDOW = True
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == '1'

# Sentry
if not DEBUG and os.environ.get('SENTRY_DNS'):
    import sentry_sdk

    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DNS'),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=0.3,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=0.3,
    )

ALLOWED_HOSTS = [
    f'{os.environ["DOMAIN"]}',
    f'.{os.environ["DOMAIN"]}',
    f'www.{os.environ["DOMAIN"]}',
    f'{os.environ["SUB"]}.{os.environ["DOMAIN"]}',
    f'{os.environ["META"]}.{os.environ["DOMAIN"]}',
]

CSRF_TRUSTED_ORIGINS = [
    f'https://{os.environ.get("DOMAIN")}',
    f'https://.{os.environ.get("DOMAIN")}',
    f'https://*.{os.environ.get("DOMAIN")}',
    f'https://www.{os.environ["DOMAIN"]}',
    f'https://{os.environ["SUB"]}.{os.environ["DOMAIN"]}',
    f'https://{os.environ["META"]}.{os.environ["DOMAIN"]}',
]

if os.environ.get('ADDITIONAL_DOMAINS'):
    for domain in os.environ.get('ADDITIONAL_DOMAINS').split(','):
        ALLOWED_HOSTS.append(f'{domain}')
        ALLOWED_HOSTS.append(f'.{domain}')
        CSRF_TRUSTED_ORIGINS.append(f'https://{domain}')
        CSRF_TRUSTED_ORIGINS.append(f'https://*.{domain}')


CORS_ORIGIN_WHITELIST = CSRF_TRUSTED_ORIGINS

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Application definition
SHARED_APPS = (
    'django_tenants',  # mandatory
    "daphne",
    'Customers',  # you must list the app where your tenant model resides in

    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # 'channels',
    'AuthBillet',
    'QrcodeCashless',
    'Administration',
    'MetaBillet',
    'root_billet',
    'wsocket',

    'django_extensions',
    'solo',
    'stdimage',
    'corsheaders',
    'django_htmx',
)

if DEBUG:
    SHARED_APPS += ('django_browser_reload',)

# CodeLogin_app/settings.py
TENANT_COLOR_ADMIN_APPS = False

TENANT_APPS = (
    # The following Django contrib apps must be in TENANT_APPS
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',

    'rest_framework_api_key',
    # your tenant-specific apps
    'BaseBillet',
    'ApiBillet',
    'PaiementStripe',
    'wsocket',
    'tibrss',
    'fedow_connect',
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]
TENANT_MODEL = "Customers.Client"  # app.Model
TENANT_DOMAIN_MODEL = "Customers.Domain"  # app.Model
ROOT_URLCONF = 'TiBillet.urls_tenants'
PUBLIC_SCHEMA_URLCONF = 'TiBillet.urls_public'
SITE_ID = 1
AUTH_USER_MODEL = 'AuthBillet.TibilletUser'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': 'memcached:11211',
    }
}

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

if DEBUG:
    MIDDLEWARE += ['django_browser_reload.middleware.BrowserReloadMiddleware',]

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
    }
]

WSGI_APPLICATION = 'TiBillet.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',  # Add 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST', 'postgres'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

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

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework_api_key.permissions.HasAPIKey",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    #     'REFRESH_TOKEN_LIFETIME': timedelta(seconds=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'fr-fr')

TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')

USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "www", "static")
STATIC_URL = '/static/'

STATICFILES_DIRS = ['BaseBillet/static', 'MetaBillet/static', 'QrcodeCashless/static', ]
# STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_ROOT = os.path.join(BASE_DIR, "www", "media")
MEDIA_URL = '/media/'

# EMAIL
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', True)

# Celery Configuration Options
CELERY_TIMEZONE = os.environ.get('TIME_ZONE', 'UTC')
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND', 'redis://redis:6379/0')
# DJANGO_CELERY_BEAT_TZ_AWARE=False

# CHANNELS
ASGI_APPLICATION = "TiBillet.asgi.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}

# -------------------------------------/
# COMMUNECTER SSO oauth2
# -------------------------------------/
OAUTH_URL_WHITELISTS = []
OAUTH_CLIENT_NAME = 'communecter'
OAUTH_CLIENT = {
    'name': 'communecter',
    'client_id': os.environ.get('COMMUNECTER_SSO_CLIENTID'),
    'client_secret': os.environ.get('COMMUNECTER_SSO_SECRET'),
    'access_token_url': 'https://sso.communecter.org/oauth/token',
    'authorize_url': 'https://sso.communecter.org/oauth/authorize',
    'api_base_url': 'https://sso.communecter.org/oauth',
    'redirect_uri': 'https://www.tibillet.org/api/user/oauth',
    'client_kwargs': {
        'scope': 'openid profile email',
        'token_placement': 'header'
    },
    'userinfo_endpoint': 'user',
}
OAUTH_COOKIE_SESSION_ID = 'sso_session_id'

# -------------------------------------/
# LLM
# -------------------------------------/

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# -------------------------------------/
# LOGGING
# -------------------------------------/

LOGGING_LVL = 'DEBUG' if DEBUG else 'INFO'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'tenant_context': {
            '()': 'django_tenants.log.TenantContextFilter'
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
            'datefmt': '%y %b %d, %H:%M:%S',
        },
        'tenant_context': {
            'format': '[%(schema_name)s:%(domain_url)s] '
                      '%(levelname)-7s %(asctime)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': LOGGING_LVL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['tenant_context'],
        },
        'logfile': {
            'level': LOGGING_LVL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f"{BASE_DIR}/logs/Djangologfile",
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
            'filters': ['tenant_context'],
        },
        'weasyprint': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f"{BASE_DIR}/logs/weasyprint",
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
            'filters': ['tenant_context'],
        },
    },
    'root': {
        'level': 'INFO',
        # 'handlers': ['console', 'logfile', 'weasyprint']
        'handlers': ['console']
    },
}


if DEBUG:
    SHELL_PLUS = "ipython"

    SHELL_PLUS_POST_IMPORTS = [  # extra things to import in notebook
        ("django.template.loader", ("get_template", "render_to_string")),
        ("IPython.lib.pretty", ("pretty")),
        ("root_billet.utils", ("pp")),
        ("datetime", ("datetime", "timedelta")),
        ("json"),
        ("requests"),
        ("fedow_connect.fedow_api", ("FedowAPI",)),
        ("fedow_connect.utils", ("rsa_generator", "sign_message", "verify_signature",
                                 "sign_utf8_string", "get_public_key", "get_private_key",
                                 "hash_hexdigest", "rsa_encrypt_string", "rsa_decrypt_string")),
        (("cryptography.hazmat.primitives"), ("serialization",)),
        (("BaseBillet.tasks"), ("test_logger",)),
        (("BaseBillet.tests"), ("BaseBilletTest",)),
        (("fedow_connect.fedow_api"), ("FedowAPI",)),
        (("django.db"), ("connection",)),

        #     ("module2.submodule", ("func1", "func2", "class1", "etc"))
        #
    ]
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"  # only use in development