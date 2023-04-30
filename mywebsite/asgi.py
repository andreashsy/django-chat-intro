"""
ASGI config for mywebsite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# from channels.routing import get_default_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mywebsite.settings")

application = ProtocolTypeRouter({
    'http': get_asgi_application(), 
    # 'http': get_default_application(), 
    'websocket':AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
})
