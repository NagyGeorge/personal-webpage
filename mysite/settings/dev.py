from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGGING["formatters"]["simple"] = {
    "format": "{levelname} {name} {message}",
    "style": "{",
}

LOGGING["handlers"]["console"]["formatter"] = "simple"

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]
