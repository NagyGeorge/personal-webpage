from django.urls import path, include
from .views import healthz

urlpatterns = [
    path('healthz/', healthz, name='healthz'),
    path('metrics/', include('django_prometheus.urls')),
]