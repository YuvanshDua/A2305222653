# shortener/models.py
from django.db import models
from django.utils import timezone

class ShortURL(models.Model):
    shortcode = models.CharField(max_length=20, unique=True, db_index=True)
    original_url = models.URLField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()
    
    def is_expired(self):
        """Checks if the short link's expiry time has passed."""
        return timezone.now() > self.expiry

class URLAnalytics(models.Model):
    short_url = models.ForeignKey(ShortURL, on_delete=models.CASCADE, related_name='analytics')
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)