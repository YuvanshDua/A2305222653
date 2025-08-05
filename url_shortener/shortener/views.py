# shortener/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import ShortURL, URLAnalytics
from .serializers import CreateShortURLSerializer, ShortURLResponseSerializer
from logging_middleware.logger import log
import random
import string

def generate_shortcode(length=6):
    """Generates a random alphanumeric shortcode."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@api_view(['POST'])
def create_short_url(request):
    serializer = CreateShortURLSerializer(data=request.data)
    if not serializer.is_valid():
        log("backend", "error", "handler", f"URL creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    if data.get('shortcode'):
        shortcode = data['shortcode']
        if ShortURL.objects.filter(shortcode=shortcode).exists():
            log("backend", "warn", "db", f"Shortcode collision: {shortcode}")
            return Response({'error': 'Shortcode already exists.'}, status=status.HTTP_409_CONFLICT)
    else:
        shortcode = generate_shortcode()
        while ShortURL.objects.filter(shortcode=shortcode).exists():
            shortcode = generate_shortcode()
            
    expiry = timezone.now() + timedelta(minutes=data['validity'])
    short_url = ShortURL.objects.create(
        original_url=data['url'], shortcode=shortcode, expiry=expiry
    )
    
    log("backend", "info", "controller", f"Created short URL: {shortcode}")
    response_serializer = ShortURLResponseSerializer(short_url, context={'request': request})
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_url_statistics(request, shortcode):
    try:
        short_url = ShortURL.objects.get(shortcode=shortcode)
    except ShortURL.DoesNotExist:
        return Response({'error': 'Shortcode not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    stats = {
        'createdAt': short_url.created_at,
        'expiryDate': short_url.expiry,
        'originalUrl': short_url.original_url,
        'clicks': short_url.analytics.count(),
    }
    return Response(stats)

def redirect_short_url(request, shortcode):
    try:
        short_url = ShortURL.objects.get(shortcode=shortcode)
        if short_url.is_expired():
            log("backend", "warn", "handler", f"Expired link accessed: {shortcode}")
            return JsonResponse({'error': 'Short link has expired.'}, status=status.HTTP_410_GONE)
        
        # Record the click for analytics
        URLAnalytics.objects.create(short_url=short_url, ip_address=request.META.get('REMOTE_ADDR'), user_agent=request.META.get('HTTP_USER_AGENT'))
        return redirect(short_url.original_url)
    except ShortURL.DoesNotExist:
        log("backend", "warn", "handler", f"Non-existent link accessed: {shortcode}")
        return JsonResponse({'error': 'Short link not found.'}, status=status.HTTP_404_NOT_FOUND)