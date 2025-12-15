#!/bin/bash

SETTINGS=absi.settings_docker
if [[ "$ENVIRONMENT" == "production" ]]; then
    SETTINGS=absi.settings_docker_production
fi

python manage.py migrate --noinput --settings=$SETTINGS

python manage.py collectstatic --noinput --clear --settings=$SETTINGS

# Start the Django application
gunicorn absi.wsgi:application \
         --env DJANGO_SETTINGS_MODULE=$SETTINGS \
         --bind 0.0.0.0:80 \
         --workers 2
