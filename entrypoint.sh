#!/bin/bash
set -e

echo "Waiting for postgres..."
while ! timeout 1 bash -c "echo > /dev/tcp/$DB_HOST/$DB_PORT" 2>/dev/null; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Waiting for redis..."
while ! timeout 1 bash -c "echo > /dev/tcp/redis/6379" 2>/dev/null; do
  sleep 0.1
done
echo "Redis started"

echo "Creating migrations..."
python manage.py makemigrations
echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
