# analytics/urls.py
from django.urls import path
from .views import URLAnalyticsAPIView, AnalyticsDashboardView, AnalyticsIndexView

urlpatterns = [
    path('', AnalyticsIndexView.as_view(), name='analytics_index'),
    path('dashboard/<str:short_code>/', AnalyticsDashboardView.as_view(), name='analytics_dashboard'),
    path('<str:short_code>/', AnalyticsDashboardView.as_view(), name='analytics_dashboard'),
    path('urls/<str:short_code>/', URLAnalyticsAPIView.as_view(), name='api_url_analytics'),
    
]