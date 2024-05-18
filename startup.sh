#!/bin/bash

# Ensure the environment variable is set
export LANG=C.UTF-8

# Start Gunicorn in the background
gunicorn --bind=0.0.0.0 --timeout 600 core.wsgi

# Start Celery worker in the background
celery -A core worker -l INFO &

# Start Celery beat scheduler in the background
celery -A core beat -l INFO &

# Update Database
python scheduletask.py &
