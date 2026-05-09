"""
Soccho Notification Service - ASGI Configuration
Properly initializes Django before importing websocket patterns
"""

import os
from django.core.asgi import get_asgi_application

# Step 1: Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_service.settings')

# Step 2: Initialize Django FIRST
# This must be called BEFORE importing any models or routing that depends on models
django_asgi_app = get_asgi_application()

# Step 3: Now import channels components
# Safe to import because Django is initialized
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from notifications.routing import websocket_urlpatterns

# Step 4: Create ASGI application with protocol routing
application = ProtocolTypeRouter({
    # HTTP requests go to Django
    "http": django_asgi_app,
    
    # WebSocket requests are handled by channels
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

# Daphne will use this application
# Command: daphne -b 0.0.0.0 -p 8000 notification_service.asgi:application
