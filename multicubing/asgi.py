import django
from django.urls import path
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from multicubing.settings import setup_settings

setup_settings()
django.setup()

from .urls import ws_urlpatterns
from .middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": TokenAuthMiddleware(
        URLRouter(
            [path(r'ws/', URLRouter(ws_urlpatterns))]
        )
    )
})
