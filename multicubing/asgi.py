import os

import django
from channels.http import AsgiHandler
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .urls import ws_urlpatterns
from .middleware import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channel.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": TokenAuthMiddleware(
        URLRouter(
            [path(r'ws/', URLRouter(ws_urlpatterns))]
        )
    )
})
