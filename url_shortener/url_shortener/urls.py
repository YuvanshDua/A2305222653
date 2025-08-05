# url_shortener/urls.py
from django.urls import path, include

urlpatterns = [
    # Include all URLs from the 'shortener' app
    path('', include('shortener.urls')),
]