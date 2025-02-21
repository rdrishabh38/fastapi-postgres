#!/bin/sh
set -e

echo "Waiting for database to become available..."
while ! nc -z postgres_db 5432; do
  sleep 1
done
echo "Database is ready!"

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
