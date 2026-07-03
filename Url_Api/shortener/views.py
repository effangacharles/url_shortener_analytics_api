# shortener/views.py
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import URL
from analytics.models import ClickAnalytics
from rest_framework.generics import CreateAPIView
from .serializers import URLSerializer

class URLRedirectView(View):
    def get(self, request, short_code):
        # 1. Fetch the long URL using the short code, or return a 404 page if it doesn't exist
        url_instance = get_object_or_404(URL, short_code=short_code)
        
        # 2. Parse User-Agent Header to extract basic browser and device info
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
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
    """
    API endpoint that allows a user to POST a long URL 
    to get back a structured shortened asset.
    """
    queryset = URL.objects.all()
    serializer_class = URLSerializer