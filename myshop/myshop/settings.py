import os
from decouple import config


DEBUG = bool(config('DEBUG'))
SECRET_KEY = config('SECRET_KEY')
SENDGRID_API_KEY = config('SENDGRID_API_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(' ')

ADMIN_EMAIL=config('ADMIN_EMAIL')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACTIVATE_TOOLBAR = True

# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'shop',
    'cart',
    'orders',
    'search',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': config('DB_HOST'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'NAME': config('DB_NAME'),
    }
}


DEFAULT_INDEX_TABLESPACE = ''

ROOT_URLCONF = 'myshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# settings for django-admin-bootstrapped
# DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static/')
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

STATIC_URL = '/static/'

# MEDIA_ROOT = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media/')

MEDIA_URL = '/media/'

CART_SESSION_ID = 'cart'

SUIT_CONFIG = {
    'ADMIN_NAME': 'Меблі Лем'
}

# CKEDITOR CONFIGURATION

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Styles', '-', 'Bold', 'Italic', 'Subscript', 'Superscript'],
            ['Undo', 'Redo', '-', 'Format', '-', 'Link'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord'],
            ['Image', '-', 'SpecialChar', 'Smiley'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyBlock', 'JustifyBlock'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['TextColor', 'BGColor', 'Blockquote', '-', 'Preview']
        ],
        'height': 500,
        'width': 800,
    },
}

if DEBUG is False:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
                'datefmt': "%d/%b/%Y %H:%M:%S",
            },
        },
        'handlers': {
            'logfile': {
                'class': 'logging.handlers.WatchedFileHandler',
                'filename': os.path.join(BASE_DIR, '..', 'logs/myshop.log'),
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['logfile'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }
# DJANGO-TOOLBAR SETTINGS
if ACTIVATE_TOOLBAR:
    INTERNAL_IPS = ('127.0.0.1', 'localhost',)
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }


FIXTURE_DIRS = (os.path.join(BASE_DIR, '..', 'fixtures'),)
