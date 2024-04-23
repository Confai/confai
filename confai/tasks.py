# tasks.py
from celery import shared_task
from .models import Ticker, ConferenceCall
from datetime import datetime
from fetch_symbols import get_calls_to_add

@shared_task
def add_todays_calls():
    todays_calls = get_calls_to_add()  # Replace this with your function to get today's calls

    for call in todays_calls:
        ticker_name = call['ticker_name']  # Replace with actual key
        quarter = call['quarter']  # Replace with actual key
        year = call['year']  # Replace with actual key

        ticker, _ = Ticker.objects.get_or_create(symbol=ticker_name)

        ConferenceCall.objects.update_or_create(
            ticker=ticker,
            year=year,
            quarter=quarter,
            defaults={
                'date': datetime.now(),  # Update the date to now
                # Add any other fields you want to update here
            }
        )