# shortener/urls.py
from django.urls import path
from .views import URLRedirectView, URLCreateAPIView, HomePageView, AnalyticsReportView

urlpatterns = [
    path('home/', HomePageView.as_view(), name='shortener_home'),
    path('analytics-report/', AnalyticsReportView.as_view(), name='analytics_report'),
    path('create_urls/', URLCreateAPIView.as_view(), name='api_url_create'),
    path('<str:short_code>/', URLRedirectView.as_view(), name='url_redirect'),
]