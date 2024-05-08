import logging
from confai.management.commands.dcf import DCF
from confai.stanalysis.sentiment import SentimentAnalyzer
from confai.models import Ticker, ConferenceCall
from datetime import datetime

logger = logging.getLogger(__name__)

def write_call(ticker_name, quarter, year):
    api = DCF()

    # Get or create the ticker object
    ticker, created = Ticker.objects.get_or_create(symbol=ticker_name)

    # Check if the call already exists in the database
    if ConferenceCall.objects.filter(ticker=ticker, year=year, quarter=quarter).exists():
        logger.info(
            f"Call for ticker: {ticker_name} for Q{quarter} {year} already exists in the database. Skipping analysis.")
        return

    # Get the transcript
    transcript = api.get_transcript(ticker_name, quarter, year)

    if transcript is None:
        logger.error(f"No transcript available for ticker: {ticker_name}")
        return

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
    logger.info(f"Added call for ticker: {ticker_name} for Q{quarter} {year}")