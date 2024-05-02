from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.

app = Celery('confai')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("Setting up periodic tasks...")
    try:
        print("Importing task...")
        from confai.tasks import add_todays_calls_task
        print("Task imported successfully")
        sender.add_periodic_task(
            crontab(minute='*/10'),  # Executes every 10 minutes
            add_todays_calls_task.s(),
        )
        print("Task added to schedule")
    except Exception as e:
        print(f"An error occurred: {e}")