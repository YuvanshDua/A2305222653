# shortener/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('shorturls', views.create_short_url),
    path('shorturls/<str:shortcode>', views.get_url_statistics),
    path('<str:shortcode>', views.redirect_short_url),
]