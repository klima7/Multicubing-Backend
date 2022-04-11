release: python manage.py migrate
web: daphne -p $PORT --bind 0.0.0.0 multicubing.asgi:application