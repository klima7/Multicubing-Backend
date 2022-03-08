release: python manage.py migrate
web: daphne -p $PORT --bind 0.0.0.0 multicubing.asgi:application
worker: celery -A multicubing worker -l INFO -B