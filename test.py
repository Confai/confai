import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

from confai.models import Ticker, ConferenceCall

# Prompt the user for a ticker name, year, and quarter
ticker_name = input("Enter a ticker name: ")

# Check if the ticker is in the database, and reprompt if it isn't
while not Ticker.objects.filter(ticker=ticker_name).exists():
    print("Ticker not found. Please try again.")
    ticker_name = input("Enter a ticker name: ")

year = int(input("Enter a year: "))
quarter = int(input("Enter a quarter: "))

# Retrieve the Ticker instance
ticker = Ticker.objects.get(ticker=ticker_name)

# Retrieve the ConferenceCall instance
call = ConferenceCall.objects.get(ticker=ticker, year=year, quarter=quarter)

# Display the requested information
print(f"Average scores: {call.average_scores}")
print(f"Extreme sentences: {call.extreme_sentences}")
print(f"Overall sentiment: {call.overall_sentiment}")
print(f"Summary: {call.summary}")