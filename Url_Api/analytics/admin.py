# analytics/admin.py
from django.contrib import admin
from .models import ClickAnalytics

@admin.register(ClickAnalytics)
class ClickAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('url', 'browser', 'device_type', 'referrer', 'clicked_at')
    list_filter = ('browser', 'device_type', 'clicked_at')
    readonly_fields = ('url', 'browser', 'device_type', 'referrer', 'clicked_at')

