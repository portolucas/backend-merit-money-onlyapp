release: python manage.py makemigrations
release: python manage.py migrate

web: gunicorn --preload merit_money.wsgi
