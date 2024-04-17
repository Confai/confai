import os
from django.core.management.base import BaseCommand
from confai.models import Ticker, ConferenceCall
from confai.sentiment import SentimentAnalyzer
from confai.summary import DocumentSummarizer
from django.conf import settings

class Command(BaseCommand):
    help = 'Load calls from a text file into the database'

    def handle(self, *args, **options):
        directory = os.path.join(settings.BASE_DIR, 'calls')
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):  # Ensure we're working with .txt files
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                    call_text = file.read()

                # The ticker name, year and quarter are in the filename
                ticker_name, year, quarter = os.path.splitext(filename)[0].replace('Y', 'Q').split('Q')
                year = int(year[-4:])  # Extract the last 4 characters for the year
                quarter = int(quarter)  # Convert the quarter to an integer

                # Get or create the Ticker instance
                ticker, created = Ticker.objects.get_or_create(name=ticker_name)

                # Analyze the call text
                analyzer = SentimentAnalyzer(call_text)
                average_scores = analyzer.get_average_scores()  # Now returns a list of strings
                highest_negative, highest_positive = analyzer.find_extreme_sentences()  # Now returns a list of strings
                overall_sentiment = analyzer.get_overall_score()  # Now returns a string

                summarizer = DocumentSummarizer(call_text)
                summary = summarizer.docsummarize()

# Get or create the ConferenceCall instance and store the sentiment analysis results
                call, created = ConferenceCall.objects.get_or_create(
                    ticker=ticker,
                    year=year,
                    quarter=quarter,
                    defaults={
                        'full_text': call_text,
                        'average_scores': average_scores,
                        'extreme_sentences': {
                            'negative': highest_negative,
                            'positive': highest_positive,
                        },
                        'overall_sentiment': overall_sentiment,
                        'summary': summary,
                    }
                )

            self.stdout.write(self.style.SUCCESS('Successfully loaded calls into the database'))