import sys

# Only import Celery if not running tests
if "test" not in sys.argv and "pytest" not in sys.modules:
    from .celery import app as celery_app

    __all__ = ("celery_app",)
else:
    __all__ = ()
