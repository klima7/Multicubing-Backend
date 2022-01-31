from django.core.wsgi import get_wsgi_application

from multicubing.settings import setup_settings

setup_settings()
application = get_wsgi_application()
