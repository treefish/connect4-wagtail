from .base import *
from environs import Env

env = Env()
env.read_env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-47u=-n7koe4tr0#f7y_$o8*g%qs54o(52k3h&7zn-*nh48$joy"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Comment this out when actually Production
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

print("*** Debug Toolbar ***")
INSTALLED_APPS = INSTALLED_APPS + [
    "debug_toolbar",
]

MIDDLEWARE = MIDDLEWARE + [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

import socket  # only if you haven't already imported this

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "172.17.0.1", "10.0.2.2"]
print("*** END Debug Toolbar ***")

# Database PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": env("SQL_ENGINE"),
        "NAME": env("SQL_DATABASE"),
        "USER": env("SQL_USER"),
        "PASSWORD": env("SQL_PASSWORD"),
        "HOST": env("SQL_HOST"),
        "PORT": env("SQL_PORT"),
    }
}

# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env("EMAIL_PORT")

# Recaptcha Settings
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_SITE_KEY")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_SECRET_KEY")
NORECAPTCHA = True

try:
    from .local import *
except ImportError:
    pass
