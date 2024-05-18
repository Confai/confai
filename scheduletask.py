import os
import django
import schedule
import time
from datetime import datetime
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

logger = logging.getLogger(__name__)

def job():
    logger.info("Job Started: Running the 'add_todays_calls' command.")
    from confai.management.commands.add_todays_calls import Command
    command = Command()
    command.handle()
    logger.info("Job Finished: The 'add_todays_calls' command has been executed.")

logger.info("Scheduling the job to run every 10 minutes.")
schedule.every(10).minutes.do(job)

next_job_time = schedule.next_run()
logger.info(f"Next job is scheduled to run at: {next_job_time}")

logger.info("Entering the main loop. This will run the scheduled jobs at their respective times.")
while True:
    current_time = datetime.now()
    if schedule.next_run() != next_job_time:
        next_job_time = schedule.next_run()
        logger.info(f"Next job is scheduled to run at: {next_job_time}")
    schedule.run_pending()
