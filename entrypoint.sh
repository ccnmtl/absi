#!/bin/bash

# TODO: Maybe call the Salt Pillar Data to populate the environment
# variables into .env locally instead of using ECS task definition
# environment variables??
# Apply Django migrations
python manage.py migrate --noinput --settings=absi.settings_docker

# Start the Django application
gunicorn absi.wsgi:application \
         --env DJANGO_SETTINGS_MODULE=absi.settings_docker \
         -b 0.0.0.0:80
