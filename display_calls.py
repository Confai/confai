import django
django.setup()

from confai.models import Ticker, ConferenceCall, TickerInfo

def get_all_calls():
    tickers = Ticker.objects.all()
    for ticker in tickers:
        ticker_info = TickerInfo.objects.get(ticker=ticker)
        calls = ConferenceCall.objects.filter(ticker=ticker_info)
        for call in calls:
            print(f"Ticker: {ticker.name}")
            print(f"Year: {ticker_info.year}")
            print(f"Quarter: {ticker_info.quarter}")
            print(f"Average scores: {call.average_scores}")
            print(f"Extreme sentences: {call.extreme_sentences}")
            print(f"Overall sentiment: {call.overall_sentiment}")
            print(f"Summary: {call.summary}")
            print("\n")
def get_conference_call_info():
    ticker_name = input("Enter a ticker name: ")
    year = int(input("Enter a year: "))
    quarter = int(input("Enter a quarter: "))

    try:
        ticker = Ticker.objects.get(name=ticker_name)
        ticker_info = TickerInfo.objects.get(ticker=ticker, year=year, quarter=quarter)
        calls = ConferenceCall.objects.filter(ticker=ticker_info)

        for call in calls:
            print(f"Ticker: {ticker.name}")
            print(f"Year: {ticker_info.year}")
            print(f"Quarter: {ticker_info.quarter}")
            print(f"Average scores: {call.average_scores}")
            print(f"Extreme sentences: {call.extreme_sentences}")
            print(f"Overall sentiment: {call.overall_sentiment}")
            print(f"Summary: {call.summary}")
            print("\n")
    except (Ticker.DoesNotExist, TickerInfo.DoesNotExist, ConferenceCall.DoesNotExist):
        print("No conference call found for the given ticker name, year, and quarter.")

get_conference_call_info()