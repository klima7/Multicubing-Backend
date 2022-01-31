from multicubing.settings import setup_settings

from django.core.asgi import get_asgi_application

setup_settings()
application = get_asgi_application()
