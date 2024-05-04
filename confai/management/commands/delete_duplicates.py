from django.core.management.base import BaseCommand
from confai.models import Ticker

class Command(BaseCommand):
    help = 'Delete duplicate tickers from the database'

    def handle(self, *args, **options):
        tickers = list(Ticker.objects.all())
        tickers_set = set()
        duplicates = []

        for ticker in tickers:
            if ticker.symbol in tickers_set:
                duplicates.append(ticker)
            else:
                tickers_set.add(ticker.symbol)

        for duplicate in duplicates:
            print(f'Deleting duplicate ticker: {duplicate.symbol}')
            duplicate.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {len(duplicates)} duplicate tickers from the database'))