#shortener/utils.py
import random
import string

def generate_shortcode(length=6):
    """Generate a random alphanumeric shortcode"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_location_from_ip(ip_address):
    """Get location from IP - simplified version"""
    # In production, use a proper GeoIP service
    return {
        'country': None,
        'region': None,
        'city': None,
        'latitude': None,
        'longitude': None
    }