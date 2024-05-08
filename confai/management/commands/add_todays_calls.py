from django.core.management.base import BaseCommand
from confai.fetch_symbols import fetch_symbols
from .writer import write_call
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Add today\'s calls to the database'

    def handle(self, *args, **options):
        logger.info("Adding today's calls to the database...")
        todays_calls = fetch_symbols()

        for call in todays_calls:
            ticker_name = call[0]  # Replace with actual key
            quarter = int(call[1][1:])  # Remove 'Q' and convert to int
            year = int(call[2])  # Convert to int
            try:
                write_call(ticker_name, quarter, year)
            except Exception as e:
                logger.error(f"Error adding call for ticker: {ticker_name} for Q{quarter} {year}")
                logger.error(e)