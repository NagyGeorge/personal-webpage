import os

import django
from django.conf import settings


def pytest_configure():
    """Configure Django settings for tests."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.dev")
    django.setup()
