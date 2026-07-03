# analytics/models.py
from django.db import models
from shortener.models import URL

class ClickAnalytics(models.Model):
    """
    Logs metadata about every single individual click redirect event.
    """
    # Cascade ensures if a URL is deleted, its analytics logs are wiped clean too
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)
    
    # We use CharFields to store raw extracted header elements
    browser = models.CharField(max_length=100, blank=True, null=True, default="Unknown")
    device_type = models.CharField(max_length=50, blank=True, null=True, default="Unknown")
    referrer = models.CharField(max_length=255, blank=True, null=True, default="Direct")

    class Meta:
        verbose_name_plural = "Click Analytics"
        ordering = ['-clicked_at']

    def __str__(self):
        return f"Click on {self.url.short_code} via {self.browser} ({self.clicked_at.strftime('%Y-%m-%d %H:%M')})"