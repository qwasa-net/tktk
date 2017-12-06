"""
Django settings for pw project.
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import configparser
import random
import string

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# read .env config
configfile = configparser.ConfigParser()
configfile.read(os.environ.get('CONFIG_FILE', os.path.join(BASE_DIR, '..', 'config.ini')))
config = configfile[os.environ.get('CONFIG_SECTION', "DEFAULT")]

# A secret key for a particular Django installation.
# This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.
SECRET_KEY = (os.getenv('SECRET_KEY')
              or config.get('SECRET_KEY')
              or "".join([random.choice(string.ascii_uppercase) for _ in range(32)]))


# A boolean that turns on/off debug mode.
DEBUG = config.getboolean("DEBUG", bool(os.getenv("DEBUG")))

# A list of strings representing the host/domain names that this Django site can serve.
ALLOWED_HOSTS = config.get("MY_HOSTS", "*").split(";")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",

    'apps.pw',
    'apps.hello'
]

if DEBUG:
    INSTALLED_APPS += ["django.contrib.staticfiles"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pw.urls"
APPEND_SLASH = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates'), ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# The path of the WSGI application that Django’s built-in servers (e.g. runserver) will use.
WSGI_APPLICATION = "pw.wsgi.application"

# Coockies
SESSION_COOKIE_NAME = 'tktk:sssn'
SESSION_COOKIE_PATH = '/'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 60*60*24*100  # 100 days

# Database (default = `../db.sqlite3`)
DATABASE_ENGINE = config.get('DATABASE_ENGINE', 'sqlite')
if DATABASE_ENGINE == 'sqlite':
    DATABASES = {
        'sqlite': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': config.get('DATABASE_NAME', os.path.join(BASE_DIR, '..', 'db.sqlite3')),
        }
    }
elif DATABASE_ENGINE in ['mysql', 'postgresql']:
    DATABASES = {
        'mysql': {
            'ENGINE': 'django.db.backends.%s' % (DATABASE_ENGINE),
            'HOST': config.get('DATABASE_HOST'),
            'NAME': config.get('DATABASE_NAME'),
            'USER': config.get('DATABASE_USER'),
            'PASSWORD': config.get('DATABASE_PASSWORD'),
        }
    }
else:
    raise Exception('invalid DATABASE engine')

DATABASES['default'] = DATABASES[DATABASE_ENGINE]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_L10N = False
USE_TZ = False


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/st/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'www', 'st')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

# Logging

LOGS_BASE_DIR = config.get("PW_LOGS_BASE_DIR", os.path.join(os.path.dirname(BASE_DIR), 'logs'))
if not os.path.exists(LOGS_BASE_DIR):
    os.makedirs(LOGS_BASE_DIR)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
            'datefmt': '%y-%m-%d %H:%M:%S'
        },
    },
    'filters': {
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue', },
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse', }
    },
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_BASE_DIR, 'debug.log'),
        },
        'production': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_BASE_DIR, 'info.log'),
        },
        'errors': {
            'level': 'ERROR',
            # 'filters': ['require_debug_false'],
            # 'class': 'django.utils.log.AdminEmailHandler',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_BASE_DIR, 'errors.log'),
        }
    },
    'loggers': {
        '': {
            'handlers': ['debug', 'production'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['debug', 'production'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['debug', 'production'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['debug', 'production', 'errors'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['debug', ],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
