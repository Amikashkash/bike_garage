web: daphne -b 0.0.0.0 -p $PORT garage.asgi:application
release: cd ui/static_src && npm install && npm run build && cd ../.. && python manage.py migrate && python manage.py setup_basic_data --noinput && python manage.py collectstatic --noinput
