from django.core.management.base import BaseCommand
from confai.fetch_symbols import fetch_symbols
from .writer import write_call

class Command(BaseCommand):
    help = 'Add today\'s calls to the database'

    def handle(self, *args, **options):
        print("Adding today's calls to the database...")
        todays_calls = fetch_symbols()

        for call in todays_calls:
            ticker_name = call[0]  # Replace with actual key
            quarter = int(call[1][1:])  # Remove 'Q' and convert to int
            year = int(call[2])  # Convert to int
            try:
                write_call(ticker_name, quarter, year)
            except Exception as e:
                print(f"Error adding call for ticker: {ticker_name} for Q{quarter} {year}")
                print(e)