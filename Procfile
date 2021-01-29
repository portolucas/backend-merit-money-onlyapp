release: python projeto_api/manage.py makemigrations --no-input
release: python projeto_api/manage.py migrate --no-input

web: gunicorn --preload projeto_api.merit_money.wsgi
