release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

worker: gunicorn ml_backend.wsgi