# Use the official Python base image
# List of public images from AWS can be located here: https://gallery.ecr.aws/docker/library/python
FROM public.ecr.aws/docker/library/python:3.13-trixie

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN rm -rf venv/
RUN rm -rf data/
RUN rm -rf *.dev.yml
RUN rm -rf .env
RUN rm -rf .dockerignore
RUN mkdir -p /var/log/django

# Expose the default Django port (change if necessary)
EXPOSE 80

RUN chmod u+x entrypoint.sh
CMD ["./entrypoint.sh"]
