# shortener/serializers.py
from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re
from .models import ShortURL

class CreateShortURLSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    validity = serializers.IntegerField(required=False, default=30, min_value=1)
    shortcode = serializers.CharField(required=False, allow_blank=True)
    
    def validate_url(self, value):
        try:
            URLValidator()(value)
        except ValidationError:
            raise serializers.ValidationError("A valid URL is required.")
        return value
        
    def validate_shortcode(self, value):
        if value and not re.match(r'^[a-zA-Z0-9_]{4,}$', value):
            raise serializers.ValidationError("Shortcode must be at least 4 alphanumeric characters.")
        return value

class ShortURLResponseSerializer(serializers.ModelSerializer):
    shortLink = serializers.SerializerMethodField()
    
    class Meta:
        model = ShortURL
        fields = ['shortLink', 'expiry']

    def get_shortLink(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/{obj.shortcode}')