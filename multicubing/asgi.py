import os

import django
from channels.http import AsgiHandler
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from multicubing.urls import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channel.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [path(r'ws/', URLRouter(ws_urlpatterns))]
        )
    )
})
