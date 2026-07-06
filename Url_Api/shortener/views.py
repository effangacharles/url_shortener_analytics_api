# shortener/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from .models import URL
from analytics.models import ClickAnalytics
from django.db.models import Count
from rest_framework.generics import CreateAPIView
from .serializers import URLSerializer


class HomePageView(View):
    def get(self, request):
        recent_clicks = ClickAnalytics.objects.select_related('url').order_by('-clicked_at')[:10]
        total_links = URL.objects.count()
        total_clicks = ClickAnalytics.objects.count()

        context = {
            'recent_clicks': recent_clicks,
            'total_links': total_links,
            'total_clicks': total_clicks,
        }
        return render(request, 'shortener.html', context)


class AnalyticsReportView(View):
    def get(self, request):
        all_clicks = ClickAnalytics.objects.select_related('url').order_by('-clicked_at')
        total_links = URL.objects.count()
        total_clicks = all_clicks.count()

        # Aggregate click counts per URL for the report summary
        link_counts = (
            ClickAnalytics.objects
            .values('url__id', 'url__short_code', 'url__long_url')
            .annotate(clicks=Count('id'))
            .order_by('-clicks')
        )

        context = {
            'all_clicks': all_clicks,
            'total_links': total_links,
            'total_clicks': total_clicks,
            'link_counts': link_counts,
        }
        return render(request, 'analytics_report.html', context)

    def post(self, request):
        ClickAnalytics.objects.all().delete()
        messages.success(request, 'All analytics records have been cleared.')
        return redirect('analytics_report')


class URLRedirectView(View):
    def get(self, request, short_code):
        # 1. Fetch the long URL using the short code, or return a 404 page if it doesn't exist
        url_instance = get_object_or_404(URL, short_code=short_code)
        
        # 2. Parse User-Agent Header to extract basic browser and device info
        user_agent = (request.META.get('HTTP_USER_AGENT') or '').lower()
        
        # Super minimal browser parsing
        if 'edg' in user_agent or 'edge' in user_agent:
            browser = 'Edge'
        elif 'chrome' in user_agent:
            browser = 'Chrome'
        elif 'firefox' in user_agent:
            browser = 'Firefox'
        elif 'safari' in user_agent:
            browser = 'Safari'
        else:
            browser = 'Other/Bot'
            
        # Super minimal device type detection
        if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
            device_type = 'Mobile'
        else:
            device_type = 'Desktop'
            
        # 3. Extract Referrer (Where did they click the link from?)
        referrer_url = request.META.get('HTTP_REFERER', 'Direct')
        # Clean up long referrer strings for cleaner dashboard metrics
        if referrer_url != 'Direct':
            try:
                from urllib.parse import urlparse
                referrer = urlparse(referrer_url).netloc
            except:
                referrer = referrer_url[:255]
        else:
            referrer = 'Direct'

        # 4. Save the analytics data to the database
        ClickAnalytics.objects.create(
            url=url_instance,
            browser=browser,
            device_type=device_type,
            referrer=referrer
        )

        # 5. Send the browser flying to the destination website!
        return redirect(url_instance.long_url)
    
class URLCreateAPIView(CreateAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer