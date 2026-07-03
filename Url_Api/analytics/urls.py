# analytics/urls.py
from django.urls import path
from .views import URLAnalyticsAPIView

urlpatterns = [
    # GET /api/urls/<short_code>/analytics/ -> Fetches metrics JSON
    path('urls/<str:short_code>/', URLAnalyticsAPIView.as_view(), name='api_url_analytics'),
    
]