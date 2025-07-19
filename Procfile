web: gunicorn garage.wsgi
release: python manage.py migrate && python manage.py setup_basic_data --noinput && python manage.py collectstatic --noinput
