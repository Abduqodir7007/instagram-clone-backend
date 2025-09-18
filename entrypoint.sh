#!/bin/sh

set -e

echo "Waiting for database"

while ! nc -z db 5432; do
    sleep 1
done 

python manage.py migrate

echo "Postgres ready"

exec "$@"
