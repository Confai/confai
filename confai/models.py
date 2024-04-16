from django.db import models
from django.contrib.postgres.fields import JSONField

class Ticker(models.Model):
    name = models.CharField(max_length=255)  # Stores the ticker name
    # Add any additional fields here

class TickerInfo(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    year = models.IntegerField()  # Stores the year of the information
    quarter = models.IntegerField()  # Stores the quarter of the information
    # Add any additional fields here

class ConferenceCall(models.Model):
    ticker = models.ForeignKey(TickerInfo, on_delete=models.CASCADE)
    full_text = models.TextField()
    average_scores = models.JSONField()  # Stores the average scores as a list of numbers
    extreme_sentences = models.JSONField()  # Stores the most positive and negative sentences as a list of strings
    overall_sentiment = models.CharField(max_length=255)  # Stores the overall sentiment as a string
    summary = models.TextField()  # Stores the summary of the conference call
