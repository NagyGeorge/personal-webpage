from django.conf import settings


def admin_settings(request):
    """Make admin settings available in all templates"""
    return {
        "ALLOWED_ADMIN_EMAIL": settings.ALLOWED_ADMIN_EMAIL,
    }
