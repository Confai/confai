from django.db import models

class Ticker(models.Model):
    name = models.CharField(max_length=255)  # Stores the ticker name
    # Add any additional fields here

class ConferenceCall(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    year = models.IntegerField(default=2024)  # Stores the year of the conference call
    quarter = models.IntegerField(default=1)  # Stores the quarter of the conference call
    full_text = models.TextField()
    average_scores = models.JSONField()  # Stores the average scores as a list of numbers
    extreme_sentences = models.JSONField()  # Stores the most positive and negative sentences as a list of strings
    overall_sentiment = models.CharField(max_length=255)  # Stores the overall sentiment as a string
    summary = models.TextField()  # Stores the summary of the conference call
