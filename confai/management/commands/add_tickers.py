import csv
from django.core.management.base import BaseCommand
from confai.models import Ticker

class Command(BaseCommand):
    help = 'Load NASDAQ tickers from screener CSV file into the database'

    def handle(self, *args, **options):
        with open(r'D:\confai\confai\management\commands\nasdaq_screen.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ticker = Ticker(
                    symbol=row['Symbol'],
                    name=row['Name'],
                    country=row['Country'],
                    sector=row['Sector'],
                    industry=row['Industry'],
                )
                ticker.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded tickers into the database'))