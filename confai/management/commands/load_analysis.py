from django.core.management.base import BaseCommand
from confai.models import Ticker, ConferenceCall
from .writer import write_call
import logging

logger = logging.getLogger(__name__)

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
                try:
                    write_call(ticker.symbol, quarter, year)
                    calls_added += 1
                    logger.info(f"Added call for ticker: {ticker.symbol} for Q{quarter} {year}")
                except Exception as e:
                    logger.error(f"Error adding call for ticker: {ticker.symbol} for Q{quarter} {year}")
                    logger.error(e)

            # Log progress and estimated time remaining
            processed_tickers = index + 1
            logger.info(f"Processed {processed_tickers} of {total_tickers} tickers.")