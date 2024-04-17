import django
django.setup()

from confai.models import Ticker, ConferenceCall

def get_all_calls():
    tickers = Ticker.objects.all()
    for ticker in tickers:
        calls = ConferenceCall.objects.filter(ticker=ticker)
        for call in calls:
            print(f"Ticker: {ticker.name}")
            print(f"Year: {call.year}")
            print(f"Quarter: {call.quarter}")
            print(f"Average scores: {call.average_scores}")
            print("Negative Extreme Sentences:")
            for sentence in call.extreme_sentences['negative']:
                print(f"Score: {sentence[0]}, Sentence: {sentence[1]}")
            print("Positive Extreme Sentences:")
            for sentence in call.extreme_sentences['positive']:
                print(f"Score: {sentence[0]}, Sentence: {sentence[1]}")
            print(f"Overall sentiment: {call.overall_sentiment}")
            print(f"Summary: {call.summary}")
            print("\n")

def get_conference_call_info():
    ticker_name = input("Enter a ticker name: ")
    year = int(input("Enter a year: "))
    quarter = int(input("Enter a quarter: "))

    try:
        ticker = Ticker.objects.get(name=ticker_name)
        calls = ConferenceCall.objects.filter(ticker=ticker, year=year, quarter=quarter)

        for call in calls:
            print(f"Ticker: {ticker.name}")
            print(f"Year: {call.year}")
            print(f"Quarter: {call.quarter}")

            print(f"Average scores: {call.average_scores}")

            negative_sentences = [(score, sentence) for score, sentence in call.extreme_sentences[0]]
            positive_sentences = [(score, sentence) for score, sentence in call.extreme_sentences[1]]
            print("Negative Extreme Sentences:")
            for score, sentence in negative_sentences:
                print(f"Score: {score}, Sentence: {sentence}")

            print("Positive Extreme Sentences:")
            for score, sentence in positive_sentences:
                print(f"Score: {score}, Sentence: {sentence}")
            print(f"Summary: {call.summary}")
            print("\n")
    except (Ticker.DoesNotExist, ConferenceCall.DoesNotExist):
        print("No conference call found for the given ticker name, year, and quarter.")

get_conference_call_info()