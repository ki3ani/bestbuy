#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --verbosity 2


# Start Gunicorn
echo "Starting server..."
exec gunicorn --bind 0.0.0.0:8000 cleanstore.wsgi:application
