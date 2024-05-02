from celery import shared_task

@shared_task
def add_todays_calls_task():
    from .management.commands.add_todays_calls import Command
    command = Command()
    command.handle()