#!/bin/bash

SETTINGS=absi.settings_docker
if [[ "$ENVIRONMENT" == "production" ]]; then
    SETTINGS=absi.settings_docker_production
fi

./ve/bin/python manage.py migrate --noinput --settings=$SETTINGS

./ve/bin/python manage.py collectstatic --noinput --clear --settings=$SETTINGS

# Start the Django application
export DJANGO_SETTINGS_MODULE=$SETTINGS
./ve/bin/daphne absi.asgi:application \
         --proxy-headers \
         --bind 0.0.0.0 --port 8000
