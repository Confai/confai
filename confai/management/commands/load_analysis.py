from django.core.management.base import BaseCommand
from confai.models import Ticker, ConferenceCall
from .writer import write_call

class Command(BaseCommand):
    help = 'Go through the database and update ConferenceCall model for each of them'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int, help='The year of the calls to add')
        parser.add_argument('quarter', type=int, help='The quarter of the calls to add')
        parser.add_argument('--start', type=str, help='The ticker symbol to start from')

    def handle(self, *args, **options):
        year = options['year']
        quarter = options['quarter']
        start_ticker = options['start']


        if start_ticker:
            tickers = list(Ticker.objects.filter(symbol__gte=start_ticker))
        else:
            tickers = list(Ticker.objects.all())

        total_tickers = len(tickers)
        for index, ticker in enumerate(tickers):

            calls_added = 0

            if not ConferenceCall.objects.filter(ticker=ticker, year=year, quarter=quarter).exists():
                write_call(ticker.symbol, quarter, year)
                calls_added += 1

            # Print progress and estimated time remaining
            processed_tickers = index + 1

            print(f"Processed {processed_tickers} of {total_tickers} tickers.")