import os
import django
import schedule
import time
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

def job():
    print("Job Started: Running the 'add_todays_calls' command.")
    from confai.management.commands.add_todays_calls import Command
    command = Command()
    command.handle()
    print("Job Finished: The 'add_todays_calls' command has been executed.")

print("Scheduling the job to run every 10 minutes.")
schedule.every(10).minutes.do(job)

next_job_time = schedule.next_run()
print(f"Next job is scheduled to run at: {next_job_time}")

print("Entering the main loop. This will run the scheduled jobs at their respective times.")
while True:
    current_time = datetime.now()
    if schedule.next_run() != next_job_time:
        next_job_time = schedule.next_run()
        print(f"Next job is scheduled to run at: {next_job_time}")
    else:
        time_remaining = next_job_time - current_time
        print(f"Time until next job runs: {time_remaining}")
    schedule.run_pending()
    time.sleep(30)