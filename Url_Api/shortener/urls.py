# shortener/urls.py
from django.urls import path
from .views import URLRedirectView, URLCreateAPIView

urlpatterns = [
    path('create_urls/', URLCreateAPIView.as_view(), name='api_url_create'),
    path('<str:short_code>/', URLRedirectView.as_view(), name='url_redirect'),
]