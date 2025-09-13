import sys

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Use SQLite for tests
if "test" in sys.argv or "pytest" in sys.modules:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }

LOGGING["formatters"]["simple"] = {
    "format": "{levelname} {name} {message}",
    "style": "{",
}

LOGGING["handlers"]["console"]["formatter"] = "simple"

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]
