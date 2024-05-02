from django.core.management.base import BaseCommand
from confai.models import Ticker, ConferenceCall
from datetime import datetime
from confai.fetch_symbols import fetch_symbols
from confai.management.commands.get_calls import DCF
from confai.stanalysis.sentiment import SentimentAnalyzer
from confai.stanalysis.summary import DocumentSummarizer
class Command(BaseCommand):
    help = 'Add today\'s calls to the database'

    def handle(self, *args, **options):
        print("Adding today's calls to the database...")
        todays_calls = self.get_todays_calls()

        api = DCF()

        for call in todays_calls:
            ticker_name = call[0]  # Replace with actual key
            quarter = int(call[1][1:])  # Remove 'Q' and convert to int
            year = int(call[2])  # Convert to int

            # Get or create the ticker object
            ticker, created = Ticker.objects.get_or_create(symbol=ticker_name)

            # Check if the call already exists in the database
            if ConferenceCall.objects.filter(ticker=ticker, year=year, quarter=quarter).exists():
                print(f"Call for ticker: {ticker_name} for Q{quarter} {year} already exists in the database. Skipping analysis.")
                continue

            # Get the transcript
            transcript = api.get_transcript(ticker_name, quarter, year)

            if transcript is None:
                print(f"No transcript available for ticker: {ticker_name}")
                continue

            # Analyze the call text
            analyzer = SentimentAnalyzer(transcript.get('content'))
            analysis = analyzer.get_analysis()

            date_str = transcript.get('date')  # Extract date from the API response
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') if date_str else None

            # Update or create the ConferenceCall instance and store the sentiment analysis results
            call, created = ConferenceCall.objects.update_or_create(
                ticker=ticker,
                year=year,
                quarter=quarter,
                defaults={
                    'full_text': transcript.get('content'),
                    'average_scores': analysis['average_scores'],
                    'extreme_sentences': analysis['extreme_sentences'],
                    'overall_sentiment': analysis['overall_score'],
                    'summary': analysis['summary'],
                    'date': date,
                    'weighted_average_sentiment': analysis['weighted_average_sentiment'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully updated ConferenceCall objects for today\'s calls'))


    def get_todays_calls(self):
        # Implement your function to get today's calls here
        return fetch_symbols()