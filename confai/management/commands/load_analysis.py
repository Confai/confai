from django.core.management.base import BaseCommand
from confai.models import Ticker, ConferenceCall
from .writer import write_call
import time

class Command(BaseCommand):
    help = 'Go through the database and update ConferenceCall model for each of them'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int, help='The year of the calls to add')
        parser.add_argument('quarter', type=int, help='The quarter of the calls to add')

    def handle(self, *args, **options):
        year = options['year']
        quarter = options['quarter']
        tickers = list(Ticker.objects.all())
        total_tickers = len(tickers)
        calls_added = 0
        start_time = time.time()

        for index, ticker in enumerate(tickers):
            if calls_added >= 450:
                elapsed_time = time.time() - start_time
                if elapsed_time < 3600:  # If less than an hour has passed
                    time.sleep(3600 - elapsed_time)  # Sleep until an hour has passed
                start_time = time.time()
                calls_added = 0

            if not ConferenceCall.objects.filter(ticker=ticker, year=year, quarter=quarter).exists():
                write_call(ticker.symbol, quarter, year)
                calls_added += 1

            # Print progress and estimated time remaining
            processed_tickers = index + 1
            remaining_tickers = total_tickers - processed_tickers
            estimated_time_remaining = remaining_tickers / 450

            print(f"Processed {processed_tickers} of {total_tickers} tickers. Estimated time remaining: {estimated_time_remaining} hours.")