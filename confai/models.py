from django.db import models
import re
class Ticker(models.Model):
    symbol = models.CharField(max_length=255, null=True)  # Stores the ticker name
    name = models.CharField(max_length=500, null=True, blank=True)  # Stores the name
    country = models.CharField(max_length=255, null=True, blank=True)  # Stores the country
    sector = models.CharField(max_length=255, null=True, blank=True)  # Stores the sector
    industry = models.CharField(max_length=255, null=True, blank=True)  # Stores the industry
    # Add any additional fields here
class ConferenceCall(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    year = models.IntegerField(default=2024)  # Stores the year of the conference call
    quarter = models.IntegerField(default=1)  # Stores the quarter of the conference call
    date = models.DateField(null=True, blank=True)
    full_text = models.TextField()
    average_scores = models.JSONField()  # Stores the average scores as a list of numbers
    extreme_sentences = models.JSONField()  # Stores the most positive and negative sentences as a list of strings
    overall_sentiment = models.CharField(max_length=255)  # Stores the overall sentiment as a string
    summary = models.TextField()  # Stores the summary of the conference call
    weighted_average_sentiment = models.FloatField(null=True, blank=True)

    @staticmethod
    def percentile(latest_call):
        lower_count = ConferenceCall.objects.filter(
            weighted_average_sentiment__lt=latest_call.weighted_average_sentiment).count()
        total_count = ConferenceCall.objects.count()
        percentile = (lower_count / total_count) * 100
        category = 'positive' if percentile > 75 else 'neutral' if percentile > 25 else 'negative'

        return percentile, category

    @staticmethod
    def format_call_text(call_text):
        # The pattern matches any sequence of word characters, followed by optional spaces, another sequence of word characters, and a colon
        pattern = r"(\w+\s*\w*:)"
        # Add a newline before each match
        formatted_text = re.sub(pattern, r'\n\n\1', call_text)
        return formatted_text