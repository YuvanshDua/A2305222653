# logging_middleware/logger.py
import requests
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJ5dXZhbnNoZHVhQGdtYWlsLmNvbSIsImV4cCI6MTc1NDM3NzY2MiwiaWF0IjoxNzU0Mzc2NzYyLCJpc3MiOiJBZmZvcmQgTWVkaWNhbCBUZWNobm9sb2dpZXMgUHJpdmF0ZSBMaW1pdGVkIiwianRpIjoiZjZhNjc3ZTQtOGE5MC00NzZhLWI5MmEtYjFiOWM0ODczYjZjIiwibG9jYWxlIjoiZW4tSU4iLCJuYW1lIjoieXV2YW5zaCBkdWEiLCJzdWIiOiJiY2I0YjBkOS05OGU5LTRhZWItOWNjOC0yNThhYjMxNTAxOGQifSwiZW1haWwiOiJ5dXZhbnNoZHVhQGdtYWlsLmNvbSIsIm5hbWUiOiJ5dXZhbnNoIGR1YSIsInJvbGxObyI6ImEyMzA1MjIyNjUzIiwiYWNjZXNzQ29kZSI6IkZ6UkdqWSIsImNsaWVudElEIjoiYmNiNGIwZDktOThlOS00YWViLTljYzgtMjU4YWIzMTUwMThkIiwiY2xpZW50U2VjcmV0IjoiRE1DV0FVSGJkYm54clpudiJ9.cu2QpTKlTA9xgtl6fdHscwlMw8JYy8hmt0HDjbsAOcA"

def log(stack, level, package, message):
    """Sends a log message to the evaluation server with authentication."""
    log_url = f"{settings.EVALUATION_SERVER_URL}/logs"
    
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    log_data = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": str(message)
    }
    
    try:
        requests.post(log_url, json=log_data, headers=headers, timeout=5)
    except Exception:
        pass

class LoggingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        """Automatically logs the outcome of an API request."""
        if response.status_code >= 500:
            log("backend", "fatal", "middleware", f"Server Error on path {request.path}")
        elif response.status_code >= 400:
            log("backend", "error", "middleware", f"Client Error on path {request.path}")
        return response