"""
URL configuration for url_shortener project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from shortener.views import URLRedirectView

from rest_framework import permissions
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

schema_view = get_schema_view(
   openapi.Info(
        title="URL Shortener & Analytics API",
        default_version='v1',
        description="API documentation for the URL Shortener and Analytics project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@e-commerce.com")
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('shortener/', include('shortener.urls')),  
    path('analytics/', include('analytics.urls')),  
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('<str:short_code>/', URLRedirectView.as_view(), name='url_redirect'),
]

# Serve static files in DEBUG (ensures drf-yasg assets are available when running runserver)
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
