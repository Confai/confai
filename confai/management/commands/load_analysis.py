from django.core.management.base import BaseCommand
from confai.models import Ticker, ConferenceCall
from confai.stanalysis.sentiment import SentimentAnalyzer
from confai.stanalysis.summary import DocumentSummarizer
from confai.management.commands.get_calls import DCF
from datetime import datetime

class Command(BaseCommand):
    help = 'Get calls for the first 100 tickers and update the ConferenceCall model for each of them'

    def handle(self, *args, **options):
        api = DCF()
        print("Getting tickers...")
        tickers = Ticker.objects.all()[:100]  # Get the first 100 tickers
        i = 0
        for ticker in tickers:
            i += 1
            call = api.get_transcript(ticker.symbol, 4, 2023)

            if call is None:
                print(f"No transcript available for call {i}, ticker: {ticker.symbol}")
                continue

            print(f"Processing call {i} : {call.get('symbol')}")

            call_text = call.get('content')  # Extract content from the API response
            year = call.get('year')  # Extract year from the API response
            quarter = call.get('quarter')  # Extract quarter from the API response
            date_str = call.get('date')  # Extract date from the API response

            # Convert the date string to a datetime object, if it's not None
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') if date_str else None

            # Analyze the call text
            analyzer = SentimentAnalyzer(call_text)
            average_scores = analyzer.get_average_scores()  # Now returns a list of strings
            highest_negative, highest_positive = analyzer.find_extreme_sentences()  # Now returns a list of strings
            overall_sentiment = analyzer.get_overall_score()  # Now returns a string
            weighted_average_sentiment = analyzer.get_weighted_average_sentiment()

            summarizer = DocumentSummarizer(call_text)
            summary = summarizer.docsummarize()

            # Update or create the ConferenceCall instance and store the sentiment analysis results
            call, created = ConferenceCall.objects.update_or_create(
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
                    'date': date,
                    'weighted_average_sentiment': weighted_average_sentiment,
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully updated ConferenceCall objects for the first 100 tickers'))