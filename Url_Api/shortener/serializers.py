# shortener/serializers.py
from rest_framework import serializers
from .models import URL

class URLSerializer(serializers.ModelSerializer):
    # This field is read-only because our signal automatically handles it
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = URL
        fields = ['id', 'long_url', 'short_code', 'short_url', 'created_at']
        read_only_fields = ['short_code', 'created_at']

    def get_short_url(self, obj):
        """
        Dynamically constructs the absolute shortcut link 
        using the current request host.
        """
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(f"/{obj.short_code}/")
        return f"/{obj.short_code}/"
    
    