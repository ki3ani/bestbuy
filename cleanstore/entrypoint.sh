#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Start server
echo "Starting server..."
exec gunicorn cleanstore.wsgi:application --bind 0.0.0.0:8000
