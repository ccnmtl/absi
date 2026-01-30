#!/bin/bash

SETTINGS=absi.settings_docker
if [[ "$ENVIRONMENT" == "production" ]]; then
    SETTINGS=absi.settings_docker_production
fi

./ve/bin/python manage.py migrate --noinput --settings=$SETTINGS

./ve/bin/python manage.py collectstatic --noinput --clear --settings=$SETTINGS

# Start the Django application
./ve/bin/gunicorn absi.asgi:application \
         --env DJANGO_SETTINGS_MODULE=$SETTINGS \
         --worker-class asgi \
         --workers 2 \
         --bind 0.0.0.0:8000
