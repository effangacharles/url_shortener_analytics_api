# shortener/admin.py
from django.contrib import admin
from .models import URL

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    # Dictates what columns show up in the admin listing interface
    list_display = ('short_code', 'long_url', 'created_at')
    # Adds a search bar targeting these specific fields
    search_fields = ('short_code', 'long_url')
    # Read-only because our signal automatically handles code generation
    readonly_fields = ('short_code',)