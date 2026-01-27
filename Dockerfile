# Use the official Python base image
# List of public images from AWS can be located here:
# https://gallery.ecr.aws/docker/library/python
FROM public.ecr.aws/docker/library/python:3.13-slim-trixie

RUN apt-get update && apt-get install -y celery

# Set the working directory in the container
WORKDIR /app

RUN mkdir -p /tmp && chmod 1777 /tmp

COPY requirements.txt .

# Upgrade pip
RUN python -m venv ve
RUN ./ve/bin/pip install --upgrade pip

# Install dependencies
RUN ./ve/bin/pip install --no-cache-dir -r requirements.txt

COPY . .
RUN rm -rf data/ *.dev.yml .env .dockerignore
RUN mkdir -p /var/log/django

# Expose the default Django port (change if necessary)
EXPOSE 80

RUN adduser --system django

RUN chown -R django:django /app
RUN chown -R django:django /var/log/django

USER django

RUN chmod u+x entrypoint.sh
CMD ["./entrypoint.sh"]
