# analytics/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from shortener.models import URL
from .models import ClickAnalytics



class URLAnalyticsAPIView(APIView):
    '''API endpoint that aggregates click logs and returns metrics.'''
    def get(self, request, short_code, *args, **kwargs):
        # Find the URL or 404
        url_instance = get_object_or_404(URL, short_code=short_code)
        
        # Aggregate clicks
        clicks = ClickAnalytics.objects.filter(url=url_instance)
        total_clicks = clicks.count()
        
        # Calculate breakdowns (e.g., Top Browsers)
        browser_breakdown = {}
        for click in clicks:
            browser_breakdown[click.browser] = browser_breakdown.get(click.browser, 0) + 1
            
        device_breakdown = {}
        for click in clicks:
            device_breakdown[click.device_type] = device_breakdown.get(click.device_type, 0) + 1

        data = {
            "short_code": short_code,
            "long_url": url_instance.long_url,
            "total_clicks": total_clicks,
            "metrics": {
                "browsers": browser_breakdown,
                "devices": device_breakdown
            },
            
        }
        return Response(data, status=status.HTTP_200_OK)