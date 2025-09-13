import logging

from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def healthz(request):
    """Health check endpoint - returns 200 only if DB and Redis are reachable"""
    status = {"status": "healthy", "checks": {}}
    is_healthy = True

    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status["checks"]["database"] = "ok"
        logger.debug("Database health check passed")
    except Exception as e:
        status["checks"]["database"] = f"error: {str(e)}"
        is_healthy = False
        logger.error(f"Database health check failed: {str(e)}")

    # Check Redis
    try:
        cache.set("health_check", "ok", 60)
        if cache.get("health_check") == "ok":
            status["checks"]["redis"] = "ok"
            logger.debug("Redis health check passed")
        else:
            status["checks"]["redis"] = "error: cache test failed"
            is_healthy = False
            logger.error("Redis health check failed: cache test failed")
    except Exception as e:
        status["checks"]["redis"] = f"error: {str(e)}"
        is_healthy = False
        logger.error(f"Redis health check failed: {str(e)}")

    if not is_healthy:
        status["status"] = "unhealthy"

    response_status = 200 if is_healthy else 503
    return JsonResponse(status, status=response_status)
