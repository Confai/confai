from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .management.commands.get_calls import Command as GetCallsCommand

@shared_task
def check_for_new_calls():
    command = GetCallsCommand()
    command.handle()