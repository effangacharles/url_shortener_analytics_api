# analytics/urls.py
from django.urls import path
from .views import URLAnalyticsAPIView

urlpatterns = [
    path('urls/<str:short_code>/', URLAnalyticsAPIView.as_view(), name='api_url_analytics'),
    
]