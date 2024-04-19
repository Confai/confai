import django

django.setup()

from confai.models import Ticker
from confai.models import ConferenceCall

def display_calls_by_ticker(ticker_symbol):
    ticker = Ticker.objects.get(symbol=ticker_symbol)
    calls = ConferenceCall.objects.filter(ticker=ticker)

    for call in calls:
        if call.year and call.quarter and call.summary and call.average_scores and call.extreme_sentences and call.overall_sentiment and call.weighted_average_sentiment:
            print(f"Year: {call.year}, Quarter: {call.quarter}, \n Summary: {call.summary}, \n Average Scores: {call.average_scores}, Extreme Sentences: {call.extreme_sentences}, Overall Sentiment: {call.overall_sentiment}, Weighted Average Sentiment: {call.weighted_average_sentiment}")
        else:
            print(f"Call information for Year: {call.year}, Quarter: {call.quarter} is incomplete.")

def display_tickers():
    tickers = Ticker.objects.all()
    for ticker in tickers:
        print(f"Symbol: {ticker.symbol}, Name: {ticker.name}, Country: {ticker.country}, Sector: {ticker.sector}, Industry: {ticker.industry}")


tickers = Ticker.objects.all()

for ticker in tickers[10:20]:
    print(ticker.symbol)
    display_calls_by_ticker(ticker.symbol)