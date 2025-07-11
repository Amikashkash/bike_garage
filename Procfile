web: gunicorn garage.wsgi
release: python manage.py migrate && python manage.py collectstatic --noinput && python fix_migrations_final.py
