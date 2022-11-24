#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z db 5432; do
      sleep 1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations home
python manage.py migrate

exec "$@"
