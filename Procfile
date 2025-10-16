web: daphne -b 0.0.0.0 -p $PORT garage.asgi:application
release: python manage.py migrate && python manage.py setup_basic_data --noinput && python manage.py collectstatic --noinput
