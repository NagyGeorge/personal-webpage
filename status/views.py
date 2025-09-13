from django.http import JsonResponse
from django.db import connections
from django.core.cache import cache
import redis


def healthz(request):
    """Health check endpoint"""
    status = {'status': 'healthy', 'checks': {}}
    
    try:
        from django.db import connection
        connection.ensure_connection()
        status['checks']['database'] = 'ok'
    except Exception as e:
        status['checks']['database'] = f'error: {str(e)}'
        status['status'] = 'unhealthy'
    
    try:
        cache.set('health_check', 'ok', 60)
        if cache.get('health_check') == 'ok':
            status['checks']['redis'] = 'ok'
        else:
            status['checks']['redis'] = 'error: cache test failed'
            status['status'] = 'unhealthy'
    except Exception as e:
        status['checks']['redis'] = f'error: {str(e)}'
        status['status'] = 'unhealthy'
    
    response_status = 200 if status['status'] == 'healthy' else 503
    return JsonResponse(status, status=response_status)